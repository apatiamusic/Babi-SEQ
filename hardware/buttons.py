# hardware/buttons.py
# Bu dosya, shift register üzerinden bağlı butonların durumlarını okuyan sınıfı içerir

from machine import Pin
import time
import config

class ButtonManager:
    """Buton durumlarını okumak için shift register kullanan sınıf"""
    
    def __init__(self, dataPin=None, clockPin=None, loadPin=None, buttonCount=None):
        """ButtonManager sınıfını başlat
        
        Args:
            dataPin: DATA pin numarası, None ise config'ten alınır
            clockPin: CLOCK pin numarası, None ise config'ten alınır
            loadPin: LOAD pin numarası, None ise config'ten alınır
            buttonCount: Buton sayısı, None ise config'ten alınır
        """
        # Pin numaralarını config'den al (eğer parametre olarak verilmemişse)
        if dataPin is None:
            dataPin = config.buttonDataPin
        if clockPin is None:
            clockPin = config.buttonClockPin
        if loadPin is None:
            loadPin = config.buttonLoadPin
        if buttonCount is None:
            buttonCount = config.buttonCount
            
        # Shift Register pinleri
        self.dataPin = Pin(dataPin, Pin.IN, Pin.PULL_UP)  # DATA/Q7 çıkışı
        self.clockPin = Pin(clockPin, Pin.OUT)           # CLOCK pini
        self.loadPin = Pin(loadPin, Pin.OUT)             # LOAD/SH pini
        
        # Toplam buton sayısı
        self.buttonCount = buttonCount
        
        # Debounce ayarları
        self.debounceTime = config.buttonDebounceTime  # ms
        self.lastButtonState = 0  # Son buton durumu (bit maskesi)
        self.lastChangeTime = 0   # Son değişiklik zamanı
        
        # Pinleri başlangıç durumlarına getir
        self.loadPin.value(1)  # LOAD pini yüksek seviyede başlat
        self.clockPin.value(0) # CLOCK pini düşük seviyede başlat
        
        print(f"ButtonManager başlatıldı: {buttonCount} buton")
    
    def getButtonState(self):
        """Tüm buton durumlarını oku (bit maskesi olarak)
        
        Returns:
            int: Her bir bit bir butonun durumunu temsil eder (1=basılı, 0=basılı değil)
        """
        return self._readShiftRegs()
    
    def _readShiftRegs(self):
        """Shift registerları oku ve buton durumunu bit maskesi olarak döndür
        
        Returns:
            int: Her bir bit bir butonun durumunu temsil eder (1=basılı, 0=basılı değil)
        """
        # Paralel yükleme için LOAD pini kısa süre düşük seviyeye çek
        self.loadPin.value(0)
        time.sleep_us(5)  # 5 mikrosaniye bekle
        self.loadPin.value(1)
        
        # Veri okuma
        buttonState = 0
        bit_values = []  # Okunan bit değerlerini kaydet (debug için)
        
        # Tüm butonları sırayla oku
        for i in range(self.buttonCount):
            # Bit değerini oku
            bit = self.dataPin.value() ^ 1  # Lojik tersine çevir (0=basılı olmayan, 1=basılı)
            bit_values.append(bit)  # Bit değerini listeye ekle (debug için)
            
            # Bit değerini maske içine yerleştir
            buttonState |= (bit << i)
            
            # Saat sinyali ver
            self.clockPin.value(1)
            time.sleep_us(5)  # 5 mikrosaniye bekle
            self.clockPin.value(0)
        
        # Durum değişti mi kontrol et
        if buttonState != self.lastButtonState:
            # Yeni buton durumu farklı
            current_time = time.ticks_ms()
            
            # Debounce süresi geçti mi?
            if time.ticks_diff(current_time, self.lastChangeTime) > self.debounceTime:
                # Değişim geçerli
                
                # DEBUG: Bit değerlerini ve buton durumunu yazdır
                if buttonState != 0:
                    # Basılı butonları bul
                    pressed_buttons = []
                    for i in range(self.buttonCount):
                        if buttonState & (1 << i):
                            pressed_buttons.append(i + 1)
                    
                    # Bir buton basıldı - bit değerlerini göster
                    bit_chunks = [bit_values[i:i+8] for i in range(0, len(bit_values), 8)]
                    print("\n--- BUTON BİT DEĞERLERİ ---")
                    for i, chunk in enumerate(bit_chunks):
                        chunk_str = " ".join([str(b) for b in chunk])
                        print(f"Bits {i*8+1}-{i*8+8}: {chunk_str}")
                    print(f"Buton durumu: 0x{buttonState:08X}")
                    print(f"Basılı butonlar: {pressed_buttons}")
                    print("-------------------------")
                
                # Durumu güncelle
                self.lastButtonState = buttonState
                self.lastChangeTime = current_time
        
        return self.lastButtonState
    
    def getPressedButtons(self):
        """Basılı olan butonların listesini döndürür
        
        Returns:
            list: Basılı butonların numaraları (1'den başlayarak)
        """
        buttonState = self.getButtonState()
        pressedButtons = []
        
        # Tüm butonları kontrol et
        for i in range(1, self.buttonCount + 1):
            if buttonState & (1 << (i - 1)):
                pressedButtons.append(i)
        
        return pressedButtons
    
    def isButtonPressed(self, buttonNumber):
        """Belirli bir butonun basılı olup olmadığını kontrol et
        
        Args:
            buttonNumber: Kontrol edilecek buton numarası (1'den başlayarak)
            
        Returns:
            bool: Buton basılı ise True, değilse False
        """
        if 1 <= buttonNumber <= self.buttonCount:
            buttonState = self.getButtonState()
            return bool(buttonState & (1 << (buttonNumber - 1)))
        return False