# features/step_config.py
# Bu dosya, adım konfigürasyonu için işlevleri sağlar

class StepConfiguration:
    """Adım konfigürasyonu için özellikler sağlayan sınıf"""
    
    def __init__(self, stepController):
        """StepConfiguration sınıfını başlat
        
        Args:
            stepController: StepController nesnesi
        """
        self.stepController = stepController
    
    def muteSelectedSteps(self):
        """Seçili adımları sessize alır
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if not self.stepController.selectedSteps:
            print("Hiçbir adım seçili değil")
            return False
        
        for step_num in self.stepController.selectedSteps:
            self.stepController.muteStep(step_num)
        
        print(f"Seçili adımlar sessize alındı: {self.stepController.selectedSteps}")
        return True
    
    def unmuteSelectedSteps(self):
        """Seçili adımların sessize alınmasını kaldırır
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if not self.stepController.selectedSteps:
            print("Hiçbir adım seçili değil")
            return False
        
        for step_num in self.stepController.selectedSteps:
            self.stepController.unmuteStep(step_num)
        
        print(f"Seçili adımların sessize alınması kaldırıldı: {self.stepController.selectedSteps}")
        return True
    
    def toggleMuteSelectedSteps(self):
        """Seçili adımların sessize alınma durumunu değiştirir
        
        Returns:
            bool: Tüm seçili adımlar sessize alındıysa True, değilse False
        """
        if not self.stepController.selectedSteps:
            # Hiçbir adım seçili değil, tüm adımların mute durumunu kontrol et
            all_muted = len(self.stepController.mutedSteps) == self.stepController.totalSteps
            
            if all_muted:
                # Tüm adımlar zaten mute, unmute yap
                self.stepController.unmuteAllSteps()
                print("Tüm adımların sessize alınması kaldırıldı")
                return False
            else:
                # Tüm adımları mute yap
                self.stepController.muteAllSteps()
                print("Tüm adımlar sessize alındı")
                return True
        
        # Seçili adımların hepsi mute mi kontrol et
        all_selected_muted = all(step in self.stepController.mutedSteps for step in self.stepController.selectedSteps)
        
        if all_selected_muted:
            # Tüm seçili adımlar zaten mute, unmute yap
            self.unmuteSelectedSteps()
            return False
        else:
            # Seçili adımları mute yap
            self.muteSelectedSteps()
            return True
    
    def soloSelectedSteps(self):
        """Seçili adımları solo yapar
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if not self.stepController.selectedSteps:
            print("Hiçbir adım seçili değil")
            return False
        
        for step_num in self.stepController.selectedSteps:
            self.stepController.soloStep(step_num)
        
        print(f"Seçili adımlar solo yapıldı: {self.stepController.selectedSteps}")
        return True
    
    def unsoloSelectedSteps(self):
        """Seçili adımların solo durumunu kaldırır
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if not self.stepController.selectedSteps:
            print("Hiçbir adım seçili değil")
            return False
        
        for step_num in self.stepController.selectedSteps:
            self.stepController.unsoloStep(step_num)
        
        print(f"Seçili adımların solo durumu kaldırıldı: {self.stepController.selectedSteps}")
        return True
    
    def toggleSoloSelectedSteps(self):
        """Seçili adımların solo durumunu değiştirir
        
        Returns:
            bool: Tüm seçili adımlar solo yapıldıysa True, değilse False
        """
        if not self.stepController.selectedSteps:
            # Hiçbir adım seçili değil, tüm solo durumunu kaldır
            if self.stepController.soloSteps:
                self.stepController.unsoloAllSteps()
                print("Tüm adımların solo durumu kaldırıldı")
            return False
        
        # Seçili adımların hepsi solo mu kontrol et
        all_selected_solo = all(step in self.stepController.soloSteps for step in self.stepController.selectedSteps)
        
        if all_selected_solo:
            # Tüm seçili adımlar zaten solo, unsolo yap
            self.unsoloSelectedSteps()
            return False
        else:
            # Seçili adımları solo yap
            self.soloSelectedSteps()
            return True
    
    def setSelectedStepsVelocity(self, velocity):
        """Seçili adımların velocity değerini ayarlar
        
        Args:
            velocity: Velocity değeri (0-127)
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if not self.stepController.selectedSteps:
            print("Hiçbir adım seçili değil")
            return False
        
        if not (0 <= velocity <= 127):
            print(f"Geçersiz velocity değeri: {velocity} (0-127 arası olmalı)")
            return False
        
        for step_num in self.stepController.selectedSteps:
            self.stepController.setStepVelocity(step_num, velocity)
        
        print(f"Seçili adımların velocity değeri ayarlandı: {velocity}")
        return True
    
    def setSelectedStepsEnvelopeParameter(self, param, value):
        """Seçili adımların envelope parametresini ayarlar
        
        Args:
            param: Envelope parametresi ('attack', 'decay', 'sustain', 'release')
            value: Parametre değeri
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if not self.stepController.selectedSteps:
            print("Hiçbir adım seçili değil")
            return False
        
        if param not in ['attack', 'decay', 'sustain', 'release']:
            print(f"Geçersiz envelope parametresi: {param}")
            return False
        
        for step_num in self.stepController.selectedSteps:
            self.stepController.setStepEnvelope(step_num, param, value)
        
        print(f"Seçili adımların {param} değeri ayarlandı: {value}")
        return True
    
    def setCMajorScale(self):
        """Tüm adımları Do Majör gamına göre ayarlar
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        # Do Majör gamı - MIDI tuş numaraları (60=C4'ten başlayarak)
        c_major_scale = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84, 86]
        
        # Tüm stepler için Do Majör gamı ayarla
        for i in range(min(16, self.stepController.totalSteps)):
            step = self.stepController.steps[i]
            
            # MIDI notasını ayarla
            step.midiNote = c_major_scale[i]
            
            # Frekansı güncelle
            step.updateFrequencyFromMidi()
        
        print("Do Majör gamı ayarlandı")
        return True