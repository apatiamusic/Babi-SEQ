# features/random_modes.py
# Bu dosya, rastgele çalma modları için işlevleri sağlar

class RandomModeManager:
    """Rastgele çalma modlarını yöneten sınıf"""
    
    def __init__(self, midiOutput):
        """RandomModeManager sınıfını başlat
        
        Args:
            midiOutput: MidiOutput nesnesi
        """
        self.midiOutput = midiOutput
    
    def toggleStandardRandomMode(self):
        """Normal rastgele modu açıp kapatır
        
        Returns:
            bool: Rastgele mod açık ise True, değilse False
        """
        return self.midiOutput.toggleRandomPlayMode()
    
    def toggleFullRandomMode(self):
        """Tam rastgele modu açıp kapatır
        
        Returns:
            bool: Tam rastgele mod açık ise True, değilse False
        """
        return self.midiOutput.toggleFullRandomMode()
    
    def resetRandomMode(self):
        """Rastgele modu kapatır
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        return self.midiOutput.resetRandomMode()
    
    def isRandomModeActive(self):
        """Herhangi bir rastgele modun aktif olup olmadığını kontrol eder
        
        Returns:
            bool: Rastgele modlardan biri aktif ise True, değilse False
        """
        return self.midiOutput.randomPlayMode or self.midiOutput.fullRandomMode
    
    def getCurrentMode(self):
        """Mevcut rastgele mod tipini döndürür
        
        Returns:
            str: "full_random", "standard_random" veya "normal"
        """
        if self.midiOutput.fullRandomMode:
            return "full_random"
        elif self.midiOutput.randomPlayMode:
            return "standard_random"
        else:
            return "normal"