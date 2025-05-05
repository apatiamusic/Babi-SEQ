# features/transpose.py
# Bu dosya, transpoze işlevlerini sağlar

class TransposeManager:
    """Transpoze işlevlerini yöneten sınıf"""
    
    def __init__(self, stepController, midiOutput):
        """TransposeManager sınıfını başlat
        
        Args:
            stepController: StepController nesnesi
            midiOutput: MidiOutput nesnesi
        """
        self.stepController = stepController
        self.midiOutput = midiOutput
        self.transposeAmount = 0
        self.transposeMode = False
    
    def toggleTransposeMode(self):
        """Transpoze modunu açıp kapatır
        
        Returns:
            bool: Transpoze modu açık ise True, değilse False
        """
        self.transposeMode = not self.transposeMode
        print(f"Transpoze modu: {'AÇIK' if self.transposeMode else 'KAPALI'}")
        return self.transposeMode
    
    def setTransposeAmount(self, semitones):
        """Transpoze miktarını ayarlar
        
        Args:
            semitones: Yarım ton sayısı (-24 ile +24 arası)
            
        Returns:
            int: Ayarlanan transpoze miktarı
        """
        # Transpoze miktarını sınırla (-24 ile +24 arası)
        self.transposeAmount = max(-24, min(24, semitones))
        
        # MidiOutput'a transpoze miktarını bildir
        self.midiOutput.setTransposeAmount(self.transposeAmount)
        
        print(f"Transpoze miktarı: {self.transposeAmount} yarım ton")
        return self.transposeAmount
    
    def adjustTransposeAmount(self, delta):
        """Transpoze miktarını değiştirir
        
        Args:
            delta: Değişim miktarı
            
        Returns:
            int: Yeni transpoze miktarı
        """
        return self.setTransposeAmount(self.transposeAmount + delta)
    
    def resetTranspose(self):
        """Transpoze miktarını sıfırlar
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        self.transposeAmount = 0
        self.midiOutput.setTransposeAmount(0)
        print("Transpoze sıfırlandı")
        return True
    
    def transposeSteps(self):
        """Adımları kalıcı olarak transpoze eder
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if self.transposeAmount == 0:
            print("Transpoze miktarı 0, işlem yapılmadı")
            return False
        
        # StepController'ı kalıcı olarak transpoze et
        result = self.stepController.transposeSteps(self.transposeAmount)
        
        if result:
            # Transpoze miktarını sıfırla
            self.transposeAmount = 0
            self.midiOutput.setTransposeAmount(0)
            print("Adımlar kalıcı olarak transpoze edildi")
        
        return result