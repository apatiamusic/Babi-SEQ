# hardware/encoders.py
# Bu dosya, rotary encoder bileşenlerini kontrol eden sınıfı içerir

from machine import Pin, Timer
import time
import config

class EncoderManager:
    """Rotary Encoder kontrolünü sağlayan sınıf"""
    
    def __init__(self, clkPin=None, dtPin=None, swPin=None, name="encoder", debounceTime=None, acceleration=True):
        """EncoderManager sınıfını başlat - Hız ivmelenme desteği ile
        
        Args:
            clkPin: CLK pini numarası, None ise config'ten alınır
            dtPin: DT pini numarası, None ise config'ten alınır
            swPin: Switch pini numarası, None ise config'ten alınır
            name: Encoder adı (tanımlama için)
            debounceTime: Debounce süresi (ms), None ise config'ten alınır
            acceleration: İvmelenme aktif mi? (hızlı çevrildiğinde daha çok değişim)
        """
        # Pin numaralarını config'den al (eğer parametre olarak verilmemişse)
        if clkPin is None:
            clkPin = config.encClk
        if dtPin is None:
            dtPin = config.encDt
        if swPin is None:
            swPin = config.encSw
            
        # Pin nesnelerini oluştur (pull-up dirençlerle)
        self.clkPin = Pin(clkPin, Pin.IN, Pin.PULL_UP)  # CLK - Saat sinyali
        self.dtPin = Pin(dtPin, Pin.IN, Pin.PULL_UP)    # DT - Veri/Yön
        self.swPin = Pin(swPin, Pin.IN, Pin.PULL_UP) if swPin is not None else None  # Switch
        
        # Pin değişikliklerini anında yakalamak için kesmeleri ayarla
        self.clkPin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self._handleClkChange)
        
        # Encoder özellikleri
        self.name = name  # Tanımlama için isim
        self.acceleration = acceleration  # İvmelenme özelliği
        
        # Config'ten debounce değerini al (eğer belirtilmemişse)
        if debounceTime is None:
            debounceTime = config.encoderDebounceTime
        
        # Encoder durumu
        self.position = 0              # Encoder pozisyonu (artma/azalma sayacı)
        self.clkLastState = self.clkPin.value()  # CLK pininin son durumu
        self.dtLastState = self.dtPin.value()    # DT pininin son durumu
        self.buttonLastState = 1       # Butonun son durumu (1=basılı değil)
        self.lastButtonTime = time.ticks_ms()  # Son buton basım zamanı
        self.lastPositionChangeTime = time.ticks_ms()  # Son pozisyon değişim zamanı
        self.debounceTime = debounceTime  # Debounce süresi (ms)
        
        # İvmelenme için değişkenler
        self.accelThreshold = 50      # İvmelenme için eşik değeri (ms)
        self.accelMultiplier = 1      # İvmelenme çarpanı (1-5 arası)
        self.consecutiveChanges = 0   # Ardışık değişim sayısı
        
        # Kesme için kullanılacak değişkenler
        self.lastInterruptTime = time.ticks_ms()
        self.lastChangeDirection = 0  # Son değişim yönü (1=CW, -1=CCW)
        self.pendingChange = 0        # Bekleyen değişiklik
        
        # Event flag
        self.buttonPressed = False    # Buton basıldı mı?
        
        # Timer ile düzenli kontrol
        self.timer = Timer(-1)
        self.timer.init(period=5, mode=Timer.PERIODIC, callback=self._checkState)
        
        print(f"EncoderManager başlatıldı: {name}")
    
    def _handleClkChange(self, pin):
        """CLK pini değişikliklerini işle (kesme fonksiyonu)"""
        # Debounce için kontrol
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.lastInterruptTime) < 5:
            return  # Debounce: çok hızlı değişimleri önle
        
        self.lastInterruptTime = current_time
        
        # Mevcut pin değerlerini oku
        clk_state = self.clkPin.value()
        dt_state = self.dtPin.value()
        
        # CLK pini değişti ve düşen kenar (1->0 geçişi) ise
        if clk_state != self.clkLastState and clk_state == 0:
            # DT pinini kontrol et - yön tespiti için
            if dt_state != clk_state:  # CLK ile DT farklı ise saat yönü
                self.pendingChange = 1
                self.lastChangeDirection = 1
            else:  # CLK ile DT aynı ise saat yönünün tersi
                self.pendingChange = -1
                self.lastChangeDirection = -1
        
        # Pin durumlarını güncelle
        self.clkLastState = clk_state
        self.dtLastState = dt_state
    
    def _checkState(self, timer):
        """Timer ile düzenli olarak durumu kontrol et"""
        # Buton kontrolü
        if self.swPin is not None:
            buttonState = self.swPin.value()
            current_time = time.ticks_ms()
            
            # Buton basıldı mı? (1->0 geçişi)
            if buttonState == 0 and self.buttonLastState == 1:
                # Debounce kontrolü
                if time.ticks_diff(current_time, self.lastButtonTime) > self.debounceTime:
                    self.lastButtonTime = current_time
                    self.buttonLastState = buttonState
                    self.buttonPressed = True
            
            # Buton bırakıldı mı? (0->1 geçişi)
            elif buttonState == 1 and self.buttonLastState == 0:
                self.buttonLastState = buttonState
    
    def update(self):
        """Encoder durumunu günceller, konum değişikliklerini takip eder
        
        Returns:
            int: Pozisyon değişimi (-N...0...+N), değişim yoksa 0
        """
        # Bekleyen bir değişiklik var mı?
        position_change = self.pendingChange
        
        if position_change != 0:
            # İvmelenme hesapla
            if self.acceleration:
                current_time = time.ticks_ms()
                time_diff = time.ticks_diff(current_time, self.lastPositionChangeTime)
                
                # Eğer aynı yönde hızlı değişim varsa ivmelenme uygula
                if time_diff < self.accelThreshold and self.lastChangeDirection == position_change:
                    self.consecutiveChanges += 1
                    # İvmelenme çarpanını hesapla (en fazla 5x)
                    self.accelMultiplier = min(5, 1 + self.consecutiveChanges // 2)
                else:
                    self.consecutiveChanges = 0
                    self.accelMultiplier = 1
                
                # Zamanı güncelle
                self.lastPositionChangeTime = current_time
                
                # İvmelenmeyi uygula
                position_change *= self.accelMultiplier
            
            # Pozisyonu güncelle
            self.position += position_change
            
            # Bekleyen değişikliği temizle
            self.pendingChange = 0
            
            return position_change
        
        return 0  # Değişim yok
    
    def checkButton(self):
        """Encoder butonunun basılıp basılmadığını kontrol eder
        
        Returns:
            bool: Buton yeni basıldıysa True, değilse False
        """
        if self.buttonPressed:
            self.buttonPressed = False
            return True
        
        return False
    
    def getPosition(self):
        """Mevcut pozisyonu döndürür
        
        Returns:
            int: Encoder pozisyonu
        """
        return self.position
    
    def resetPosition(self, newPosition=0):
        """Encoder pozisyonunu sıfırlar veya belirli bir değere ayarlar
        
        Args:
            newPosition: Yeni pozisyon değeri (varsayılan: 0)
        """
        self.position = newPosition
    
    def deinit(self):
        """Encoder'ı kapatır - timer ve kesmeleri temizler"""
        # Timer ve kesmeleri temizle
        if self.timer:
            self.timer.deinit()
        
        # Kesmeleri kaldır
        self.clkPin.irq(handler=None)