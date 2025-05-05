# features/envelope.py
# Bu dosya, ADSR envelope kontrolü işlevlerini sağlar

class EnvelopeManager:
    """ADSR envelope yönetimi sınıfı"""
    
    def __init__(self, stepController):
        """EnvelopeManager sınıfını başlat
        
        Args:
            stepController: StepController nesnesi
        """
        self.stepController = stepController
        self.currentParameter = 'attack'  # 'attack', 'decay', 'sustain', 'release'
    
    def selectParameter(self, parameter):
        """Envelope parametresini seç
        
        Args:
            parameter: Envelope parametresi ('attack', 'decay', 'sustain', 'release')
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if parameter in ['attack', 'decay', 'sustain', 'release']:
            self.currentParameter = parameter
            print(f"Envelope parametresi seçildi: {parameter}")
            return True
        else:
            print(f"Geçersiz envelope parametresi: {parameter}")
            return False
    
    def cycleParameter(self):
        """Bir sonraki envelope parametresine geç
        
        Returns:
            str: Yeni seçilen parametre adı
        """
        parameters = ['attack', 'decay', 'sustain', 'release']
        current_index = parameters.index(self.currentParameter)
        next_index = (current_index + 1) % len(parameters)
        self.currentParameter = parameters[next_index]
        print(f"Envelope parametresi değiştirildi: {self.currentParameter}")
        return self.currentParameter
    
    def adjustParameter(self, delta):
        """Seçili parametreyi ayarla
        
        Args:
            delta: Değişim miktarı
            
        Returns:
            int: Ayarlanan değer, işlem başarısız olursa -1
        """
        if not self.stepController.selectedSteps:
            print("Hiçbir adım seçili değil")
            return -1
        
        return self.stepController.adjustSelectedEnvelope(self.currentParameter, delta)
    
    def setParameter(self, value):
        """Seçili parametreyi belirli bir değere ayarla
        
        Args:
            value: Yeni parametre değeri
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if not self.stepController.selectedSteps:
            print("Hiçbir adım seçili değil")
            return False
        
        # Parametre değerini sınırla
        if self.currentParameter == 'attack':
            value = max(1, min(1000, value))  # 1-1000 ms
        elif self.currentParameter == 'decay':
            value = max(1, min(2000, value))  # 1-2000 ms
        elif self.currentParameter == 'sustain':
            value = max(0, min(100, value))   # 0-100 %
        elif self.currentParameter == 'release':
            value = max(1, min(3000, value))  # 1-3000 ms
        
        for step_num in self.stepController.selectedSteps:
            self.stepController.setStepEnvelope(step_num, self.currentParameter, value)
        
        print(f"Seçili adımların {self.currentParameter} değeri ayarlandı: {value}")
        return True
    
    def getParameterValues(self):
        """Seçili adımların envelope parametre değerlerini döndürür
        
        Returns:
            dict: Envelope parametre değerleri, hiç adım seçili değilse None
        """
        if not self.stepController.selectedSteps:
            print("Hiçbir adım seçili değil")
            return None
        
        # İlk seçili adımın envelope değerlerini döndür
        first_step = min(self.stepController.selectedSteps)
        return self.stepController.getStepEnvelope(first_step)