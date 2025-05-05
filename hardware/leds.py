# hardware/leds.py
# Bu dosya, WS2812B RGB LED şeridini kontrol eden sınıfı içerir

from machine import Pin
import neopixel
import time
import config

class LEDManager:
    """WS2812B RGB LED şeridini yöneten sınıf"""
    
    # Renk sabitleri
    #Kırmızı, Mavi, Yeşil
    OFF = (0, 0, 0)           # Kapalı
    DARK_BLUE = (0, 64, 0)    # Koyu mavi (aktif step)
    PURPLE = (32, 32, 0)      # Mor (aktif olmayan step)
    RED = (50, 0, 0)          # Kırmızı (çalınan adım)
    ORANGE = (50, 0, 20)      # Turuncu (mute)
    WHITE = (50, 50, 50)      # Beyaz (Selected)
    
    def __init__(self, ledPin=None, ledCount=None):
        """LED yöneticisini başlat
        
        Args:
            ledPin: LED veri pini, None ise config'ten alınır
            ledCount: LED sayısı, None ise config'ten alınır
        """
        # Pin numarasını config'den al (eğer parametre olarak verilmemişse)
        if ledPin is None:
            ledPin = config.ledStripPin
        if ledCount is None:
            ledCount = config.ledStripCount
            
        # LED şeridini başlat
        self.pin = Pin(ledPin, Pin.OUT)
        self.np = neopixel.NeoPixel(self.pin, ledCount)
        self.ledCount = ledCount
        
        # Durum değişkenleri
        self.activeSteps = 16  # Aktif adım sayısı (varsayılan 16)
        self.selectedSteps = set()  # Seçili adımlar
        self.currentStep = -1  # Şu an çalınan adım
        self.mutedSteps = set()  # Sessiz adımlar
        self.soloSteps = set()  # Solo adımlar
        self.velocities = {}   # Step velocity değerleri
        
        # İlk açılışta tüm ledleri ayarla
        self.initialSetup()
        
        print(f"LEDManager başlatıldı: {ledCount} LED")
    
    def initialSetup(self):
        """Cihaz açıldığında LEDleri ayarla"""
        # İlk 16 LED koyu mavi, diğer 16 LED mor renkte
        for i in range(self.ledCount):
            if i < self.activeSteps:
                self.np[i] = self.DARK_BLUE
            else:
                self.np[i] = self.PURPLE
        self.np.write()
    
    def clear(self):
        """Tüm LED'leri kapat"""
        for i in range(self.ledCount):
            self.np[i] = self.OFF
        self.np.write()
    


    def update(self, activeSteps=None, selectedSteps=None, currentStep=None, mutedSteps=None, soloSteps=None, velocities=None):
        """LED'leri güncelle
        
        Args:
            activeSteps: Aktif adım sayısı
            selectedSteps: Seçili adımlar kümesi
            currentStep: Şu an çalınan adım
            mutedSteps: Sessiz adımlar kümesi
            soloSteps: Solo adımlar kümesi
            velocities: Step velocity değerleri sözlüğü
        """
        # Parametreleri güncelle (None olmayanları)
        if activeSteps is not None:
            self.activeSteps = activeSteps
        if selectedSteps is not None:
            self.selectedSteps = selectedSteps
        if currentStep is not None:
            self.currentStep = currentStep
        if mutedSteps is not None:
            self.mutedSteps = mutedSteps
        if soloSteps is not None:
            self.soloSteps = soloSteps
        if velocities is not None:
            self.velocities = velocities
        
        # Solo modu aktif mi kontrol et
        solo_mode = len(self.soloSteps) > 0
        
        # Tüm LED'leri güncelle
        for i in range(self.ledCount):
            # 1-tabanlı adım numarası (LED'ler 0-tabanlı)
            step_num = i + 1
            
            # Adım aktif mi?
            is_active = step_num <= self.activeSteps
            
            # Adım seçili mi?
            is_selected = step_num in self.selectedSteps
            
            # Mevcut çalınan adım mı?
            is_current = (i == self.currentStep)
            
            # Adım sessiz mi?
            is_muted = step_num in self.mutedSteps
            
            # Adım solo mu?
            is_solo = step_num in self.soloSteps
            
            # LED rengini belirle (öncelik sıralamasına dikkat!)
            if is_current:
                # Çalınan adım - kırmızı (en yüksek öncelik)
                color = self.RED
            elif solo_mode:
                if is_solo:
                    # Solo modunda solo adım - koyu mavi
                    color = self.DARK_BLUE
                else:
                    # Solo modunda olmayan adım - turuncu (sessiz)
                    color = self.ORANGE
            elif is_muted:
                # Sessiz adım - turuncu
                color = self.ORANGE
            elif is_selected:
                # Seçili adım ve mute/solo durumunda değil - beyaz
                color = self.WHITE
            elif is_active:
                # Aktif adım - koyu mavi
                color = self.DARK_BLUE
            else:
                # Aktif olmayan adım - mor
                color = self.PURPLE
            
            # Velocity ayarlaması
            if step_num in self.velocities and is_active:
                # Velocity değeri 0-127 arasında, bunu parlaklık için kullan
                brightness = self.velocities[step_num] / 127.0
                color = tuple(int(c * brightness) for c in color)
            
            # LED'i güncelle
            self.np[i] = color
        
        # LED'leri güncelle
        self.np.write()
        
    def setCurrentStep(self, step):
        """Çalınan adımı güncelle
        
        Args:
            step: Çalınan adım (0-tabanlı)
        """
        self.currentStep = step
        self.update()
    
    def setSelectedSteps(self, steps):
        """Seçili adımları güncelle
        
        Args:
            steps: Seçili adımlar kümesi (1-tabanlı)
        """
        self.selectedSteps = steps
        self.update()
    
    def setActiveSteps(self, count):
        """Aktif adım sayısını güncelle
        
        Args:
            count: Aktif adım sayısı
        """
        self.activeSteps = count
        self.update()
    
    def setMutedSteps(self, steps):
        """Sessiz adımları güncelle
        
        Args:
            steps: Sessiz adımlar kümesi (1-tabanlı)
        """
        self.mutedSteps = steps
        self.update()
    
    def setSoloSteps(self, steps):
        """Solo adımları güncelle
        
        Args:
            steps: Solo adımlar kümesi (1-tabanlı)
        """
        self.soloSteps = steps
        self.update()
        
    def setVelocities(self, velocities):
        """Step velocity değerlerini güncelle
        
        Args:
            velocities: Step velocity değerleri sözlüğü
        """
        self.velocities = velocities
        self.update()
    
    def blinkStep(self, step, color=None, duration=0.1):
        """Bir adımı belirli bir renkte yanıp söndür
        
        Args:
            step: Adım numarası (1-tabanlı)
            color: Renk (R, G, B), None ise kırmızı kullanılır
            duration: Yanıp sönme süresi (saniye)
        """
        if color is None:
            color = self.RED
        
        # Adımı 0-tabanlı indekse dönüştür
        led_index = step - 1
        
        # LED indeksinin geçerli olduğunu kontrol et
        if 0 <= led_index < self.ledCount:
            # Mevcut rengi sakla
            old_color = self.np[led_index]
            
            # Yeni rengi ayarla
            self.np[led_index] = color
            self.np.write()
            
            # Belirtilen süre kadar bekle
            time.sleep(duration)
            
            # Eski rengi geri getir
            self.np[led_index] = old_color
            self.np.write()