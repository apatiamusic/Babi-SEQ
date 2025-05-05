# sequencer/step_controller.py
# Bu dosya, sequencer'ın temel mantığını ve adım işlemlerini içerir

import math
import config
from sequencer.utils import midiToFreq, getNoteName

class Step:
    """Sequencer adımını temsil eden sınıf"""
    
    def __init__(self, number, defaultMidiNote=None):
        """Step sınıfını başlat
        
        Args:
            number: Adım numarası (1-tabanlı)
            defaultMidiNote: Varsayılan MIDI nota numarası, None ise config'ten alınır
        """
        if defaultMidiNote is None:
            defaultMidiNote = config.defaultMidiNote
            
        self.number = number
        self.midiNote = defaultMidiNote
        self.frequency = midiToFreq(defaultMidiNote)
        self.velocity = 100
        self.isSelected = False
        self.isMuted = False
        self.isSolo = False
        self.isActive = True
        
        # Envelope (ADSR) değerleri
        self.envelope = {
            'attack': 10,    # ms
            'decay': 100,    # ms
            'sustain': 70,   # %
            'release': 100   # ms
        }
    
    def getMidiNoteName(self):
        """MIDI nota adını döndürür
        
        Returns:
            str: MIDI nota adı (örn. "C4", "A#5")
        """
        return getNoteName(self.midiNote)
    
    def updateFrequencyFromMidi(self):
        """MIDI nota değerinden frekansı günceller"""
        self.frequency = midiToFreq(self.midiNote)
    
    def updateMidiFromFrequency(self):
        """Frekans değerinden MIDI nota değerini günceller"""
        from sequencer.utils import freqToMidi  # functions yerine sequencer.utils'i import et
        self.midiNote = freqToMidi(self.frequency)

class StepController:
    """Sequencer adımlarını kontrol eden sınıf"""
    
    def __init__(self, totalSteps=None):
        """StepController sınıfını başlat
        
        Args:
            totalSteps: Toplam adım sayısı, None ise config'ten alınır
        """
        # Config'ten değerleri al (eğer parametre olarak verilmemişse)
        if totalSteps is None:
            totalSteps = config.defaultStepCount
            
        self.totalSteps = totalSteps
        self.defaultMidiNote = config.defaultMidiNote
        
        # Step nesneleri listesi
        self.steps = []
        for i in range(1, totalSteps + 1):
            self.steps.append(Step(i, self.defaultMidiNote))
        
        # Hangi stepler seçili? (1-tabanlı adım numaraları)
        self.selectedSteps = set()
        
        # Mute ve Solo özelliği için adım kümeleri (1-tabanlı adım numaraları)
        self.mutedSteps = set()
        self.soloSteps = set()
        
        # Frekans modu: True = doğrudan frekans, False = MIDI tuş numarası
        self.frequencyMode = False  # Varsayılan olarak MIDI modu
        
        # LED yöneticisi referansı (app.py'den atanacak)
        self.ledManager = None
        
        # Son işlenen buton
        self.lastProcessedButton = None
        
        print(f"StepController başlatıldı: {totalSteps} adımlı sequencer")
    
    def setLedManager(self, ledManager):
        """LED yöneticisini ayarla
        
        Args:
            ledManager: LEDManager nesnesi
        """
        self.ledManager = ledManager
    
    def selectStep(self, stepNumber, clearOthers=True):
        """Bir adımı seçili hale getirir veya seçimden kaldırır
        
        Args:
            stepNumber: Adım numarası (1-tabanlı)
            clearOthers: Diğer seçimleri temizle
        """
        if 1 <= stepNumber <= self.totalSteps:
            # Son işlenen butonu güncelle
            self.lastProcessedButton = stepNumber
            
            # Eğer clearOthers aktifse ve step zaten seçili değilse
            if clearOthers and stepNumber not in self.selectedSteps:
                # Önceki seçimleri temizle
                self.selectedSteps.clear()
                for step in self.steps:
                    step.isSelected = False
                
            # Eğer zaten seçiliyse, seçimi kaldır
            if stepNumber in self.selectedSteps:
                self.selectedSteps.remove(stepNumber)
                self.steps[stepNumber-1].isSelected = False
                print(f"Step {stepNumber} seçimi kaldırıldı")
            else:
                # Seçili değilse, seç
                self.selectedSteps.add(stepNumber)
                self.steps[stepNumber-1].isSelected = True
                self._printStepInfo(stepNumber)
                
            self.updateLeds()
            
            # LED manager mevcutsa seçili adımları güncelle
            if self.ledManager:
                self.ledManager.setSelectedSteps(self.selectedSteps)
    
    def selectAllSteps(self):
        """Tüm adımları seçili hale getirir"""
        if len(self.selectedSteps) == self.totalSteps:
            # Eğer zaten tümü seçiliyse, tüm seçimleri kaldır
            self.selectedSteps.clear()
            for step in self.steps:
                step.isSelected = False
            print("Tüm seçimler kaldırıldı")
        else:
            # Tüm adımları seç
            self.selectedSteps = set(range(1, self.totalSteps + 1))
            for step in self.steps:
                step.isSelected = True
            print("Tüm stepler seçildi")
            
            # Tüm seçili steplerin bilgilerini göster
            for step_num in sorted(self.selectedSteps):
                self._printStepInfo(step_num)
        
        # Son işlenen butonu sıfırla
        self.lastProcessedButton = None
        self.updateLeds()
    
    def toggleSelectionWithEncoderSwitch(self):
        """Encoder switch için seçim fonksiyonu - boşsa tümünü seç, doluysa temizle"""
        if self.selectedSteps:
            # Eğer seçili step varsa, tüm seçimleri temizle
            self.selectedSteps.clear()
            for step in self.steps:
                step.isSelected = False
            print("Tüm seçimler temizlendi")
        else:
            # Seçili step yoksa, tüm adımları seç
            self.selectedSteps = set(range(1, self.totalSteps + 1))
            for step in self.steps:
                step.isSelected = True
            print("Tüm stepler seçildi")
            
            # Seçili adımların bilgilerini göster
            for step_num in sorted(self.selectedSteps):
                self._printStepInfo(step_num)
        
        self.lastProcessedButton = None
        self.updateLeds()
        
        # LED manager mevcutsa seçili adımları güncelle
        if self.ledManager:
            self.ledManager.setSelectedSteps(self.selectedSteps)
    
    def clearSelection(self):
        """Tüm seçimleri temizler"""
        self.selectedSteps.clear()
        for step in self.steps:
            step.isSelected = False
        self.lastProcessedButton = None
        self.updateLeds()
        print("Tüm seçimler temizlendi")
    
    def toggleFrequencyMode(self):
        """Frekans modunu değiştirir (MIDI <-> doğrudan frekans)"""
        self.frequencyMode = not self.frequencyMode
        
        modeText = "doğrudan frekans" if self.frequencyMode else "MIDI tuş numarası"
        print(f"Frekans modu değiştirildi: {modeText}")
        
        # Seçili adımların bilgilerini güncelle
        for step_num in sorted(self.selectedSteps):
            self._printStepInfo(step_num)
            
        return self.frequencyMode
    
    def adjustValue(self, delta):
        """Seçili steplerin değerlerini değiştirir
        
        Args:
            delta: Değişim miktarı
        
        Returns:
            bool: Değişiklik olduysa True, olmadıysa False
        """
        if not self.selectedSteps:
            print("Hiçbir step seçili değil!")
            return False
            
        changed = False
        
        for step_num in self.selectedSteps:
            step = self.steps[step_num-1]
            
            if self.frequencyMode:
                # Doğrudan frekans modunda - birer birer değişim
                oldFreq = step.frequency
                # Delta'yı 1 veya -1 olarak normalize et
                normDelta = 1 if delta > 0 else -1 if delta < 0 else 0
                step.frequency += normDelta
                
                # Negatif frekans olmasın
                if step.frequency < 1:
                    step.frequency = 1
                
                # MIDI değerini güncelle (yaklaşık)
                step.updateMidiFromFrequency()
                
                if oldFreq != step.frequency:
                    changed = True
                
            else:
                # MIDI tuş numarası modunda
                oldMidi = step.midiNote
                step.midiNote += delta
                
                # MIDI aralığını sınırla (0-127)
                if step.midiNote < 0:
                    step.midiNote = 0
                elif step.midiNote > 127:
                    step.midiNote = 127
                
                # Frekansı güncelle
                step.updateFrequencyFromMidi()
                
                if oldMidi != step.midiNote:
                    changed = True
        
        # Değişiklik olduysa sonuçları yazdır
        if changed:
            for step_num in sorted(self.selectedSteps):
                self._printStepInfo(step_num)
                
        return changed
    
    def _printStepInfo(self, stepNumber):
        """Adım bilgilerini yazdırır
        
        Args:
            stepNumber: Adım numarası (1-tabanlı)
        """
        if 1 <= stepNumber <= self.totalSteps:
            step = self.steps[stepNumber-1]
            
            # Nota ismi hesapla
            noteName = step.getMidiNoteName()
            
            if self.frequencyMode:
                print(f"Step {stepNumber}: {step.frequency:.2f} Hz (yaklaşık {noteName}, MIDI: {step.midiNote})")
            else:
                print(f"Step {stepNumber}: MIDI {step.midiNote} ({noteName}, {step.frequency:.2f} Hz)")
    
    def updateLeds(self):
        """LED'leri günceller (seçili adımlar yanar)"""
        if self.ledManager:
            self.ledManager.setSelectedSteps(self.selectedSteps)
    
    def updateMidiFromFreq(self):
        """Frekans değerlerinden MIDI notalarını günceller"""
        for step in self.steps:
            step.updateMidiFromFrequency()
        
        print("MIDI notaları frekanslardan güncellendi")
        return True
    
    def getPatternData(self):
        """Mevcut pattern verilerini döndürür
        
        Returns:
            dict: Pattern verilerini içeren sözlük
        """
        pattern_data = {
            "steps": []
        }
        
        for step in self.steps:
            step_data = {
                "step": step.number,
                "frequency": step.frequency,
                "midiNote": step.midiNote,
                "velocity": step.velocity,
                "envelope": step.envelope
            }
            pattern_data["steps"].append(step_data)
        
        return pattern_data
    
    def loadPatternData(self, pattern_data):
        """Pattern verilerini yükler
        
        Args:
            pattern_data: Pattern verilerini içeren sözlük
            
        Returns:
            bool: Yükleme başarılıysa True, değilse False
        """
        try:
            # Basit pattern formatı (doğrudan steps dizisi)
            if "steps" in pattern_data:
                steps_data = pattern_data["steps"]
                total_steps = min(len(steps_data), self.totalSteps)
                
                for i in range(total_steps):
                    step_data = steps_data[i]
                    
                    # Step numarası 1'den başlıyor olabilir
                    step_num = step_data.get("step", i+1)
                    step_index = step_num - 1 if step_num else i
                    
                    # Geçerli bir indeks mi kontrol et
                    if 0 <= step_index < self.totalSteps:
                        step = self.steps[step_index]
                        
                        # Frekans değeri
                        if "frequency" in step_data:
                            step.frequency = step_data["frequency"]
                        
                        # MIDI nota değeri
                        if "midiNote" in step_data:
                            step.midiNote = step_data["midiNote"]
                            
                        # Velocity değeri
                        if "velocity" in step_data:
                            step.velocity = step_data["velocity"]
                            
                        # Envelope değerleri
                        if "envelope" in step_data:
                            step.envelope.update(step_data["envelope"])
                
                # Frekanslardan MIDI notalarını güncelle
                self.updateMidiFromFreq()
                
                # LED'leri güncelle
                self.updateLeds()
                
                print("Pattern başarıyla yüklendi")
                return True
            else:
                print("Geçersiz pattern formatı - 'steps' alanı bulunamadı")
                return False
        except Exception as e:
            print(f"Pattern yükleme hatası: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def muteStep(self, stepNumber):
        """Bir adımı sessize alır
        
        Args:
            stepNumber: Adım numarası (1-tabanlı)
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if 1 <= stepNumber <= self.totalSteps:
            self.mutedSteps.add(stepNumber)
            self.steps[stepNumber-1].isMuted = True
            print(f"Step {stepNumber} sessize alındı")
            
            # LED manager mevcutsa muted adımları güncelle
            if self.ledManager:
                self.ledManager.setMutedSteps(self.mutedSteps)
                
            return True
        return False
    
    def unmuteStep(self, stepNumber):
        """Bir adımın sessize alınmasını kaldırır
        
        Args:
            stepNumber: Adım numarası (1-tabanlı)
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if stepNumber in self.mutedSteps:
            self.mutedSteps.remove(stepNumber)
            self.steps[stepNumber-1].isMuted = False
            print(f"Step {stepNumber} sessize alınması kaldırıldı")
            
            # LED manager mevcutsa muted adımları güncelle
            if self.ledManager:
                self.ledManager.setMutedSteps(self.mutedSteps)
                
            return True
        return False
    
    def muteAllSteps(self):
        """Tüm adımları sessize alır
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        self.mutedSteps = set(range(1, self.totalSteps + 1))
        for step in self.steps:
            step.isMuted = True
        print("Tüm adımlar sessize alındı")
        
        # LED manager mevcutsa muted adımları güncelle
        if self.ledManager:
            self.ledManager.setMutedSteps(self.mutedSteps)
            
        return True
    
    def unmuteAllSteps(self):
        """Tüm adımların sessize alınmasını kaldırır
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        self.mutedSteps.clear()
        for step in self.steps:
            step.isMuted = False
        print("Tüm adımların sessize alınması kaldırıldı")
        
        # LED manager mevcutsa muted adımları güncelle
        if self.ledManager:
            self.ledManager.setMutedSteps(self.mutedSteps)
            
        return True
    
    def soloStep(self, stepNumber):
        """Bir adımı solo yapar
        
        Args:
            stepNumber: Adım numarası (1-tabanlı)
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if 1 <= stepNumber <= self.totalSteps:
            self.soloSteps.add(stepNumber)
            self.steps[stepNumber-1].isSolo = True
            print(f"Step {stepNumber} solo yapıldı")
            
            # LED manager mevcutsa solo adımları güncelle
            if self.ledManager:
                self.ledManager.setSoloSteps(self.soloSteps)
                
            return True
        return False
    
    def unsoloStep(self, stepNumber):
        """Bir adımın solo durumunu kaldırır
        
        Args:
            stepNumber: Adım numarası (1-tabanlı)
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if stepNumber in self.soloSteps:
            self.soloSteps.remove(stepNumber)
            self.steps[stepNumber-1].isSolo = False
            print(f"Step {stepNumber} solo durumu kaldırıldı")
            
            # LED manager mevcutsa solo adımları güncelle
            if self.ledManager:
                self.ledManager.setSoloSteps(self.soloSteps)
                
            return True
        return False
    
    def soloAllSteps(self):
        """Tüm adımları solo yapar
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        self.soloSteps = set(range(1, self.totalSteps + 1))
        for step in self.steps:
            step.isSolo = True
        print("Tüm adımlar solo yapıldı")
        
        # LED manager mevcutsa solo adımları güncelle
        if self.ledManager:
            self.ledManager.setSoloSteps(self.soloSteps)
            
        return True
    
    def unsoloAllSteps(self):
        """Tüm adımların solo durumunu kaldırır
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        self.soloSteps.clear()
        for step in self.steps:
            step.isSolo = False
        print("Tüm adımların solo durumu kaldırıldı")
        
        # LED manager mevcutsa solo adımları güncelle
        if self.ledManager:
            self.ledManager.setSoloSteps(self.soloSteps)
            
        return True
    
    def isStepAudible(self, stepNumber):
        """Bir adımın çalınabilir olup olmadığını kontrol eder
        
        Args:
            stepNumber: Adım numarası (1-tabanlı)
        
        Returns:
            bool: Adım çalınabilirse True, değilse False
        """
        # Solo mod aktif mi?
        solo_mode_active = len(self.soloSteps) > 0
        
        if solo_mode_active:
            # Solo mod aktifse, sadece solo adımlar çalınabilir
            return stepNumber in self.soloSteps
        else:
            # Solo mod aktif değilse, mute olmayan adımlar çalınabilir
            return stepNumber not in self.mutedSteps
    
    def setStepVelocity(self, stepNumber, velocity):
        """Bir adımın velocity değerini ayarlar
        
        Args:
            stepNumber: Step numarası (1-tabanlı)
            velocity: Yeni velocity değeri (0-127)
        
        Returns:
            bool: İşlem başarılı mı?
        """
        if 1 <= stepNumber <= self.totalSteps:
            step_index = stepNumber - 1
            self.steps[step_index].velocity = velocity
            
            # LED yöneticisini güncelle
            if hasattr(self, 'ledManager') and self.ledManager:
                velocities = {stepNumber: velocity}
                self.ledManager.setVelocities(velocities)
            
            return True
        return False
    
    
    def getStepVelocity(self, stepNumber):
        """Bir adımın velocity değerini döndürür
        
        Args:
            stepNumber: Adım numarası (1-tabanlı)
        
        Returns:
            int: Velocity değeri (0-127)
        """
        if 1 <= stepNumber <= self.totalSteps:
            return self.steps[stepNumber-1].velocity
        return 100  # Varsayılan değer
    
    def adjustSelectedVelocities(self, delta):
        """Seçili adımların velocity değerlerini değiştirir
        
        Args:
            delta: Değişim miktarı
        
        Returns:
            int: İlk seçili adımın yeni velocity değeri, veya hiç adım seçili değilse -1
        """
        if not self.selectedSteps:
            print("Hiçbir step seçili değil!")
            return -1
        # Velocity değişimini 5 ile çarp
        delta = delta * 5
        
        velocities = {}  # LED güncelleme için velocity değerlerini topla
        
        for step_num in self.selectedSteps:
            step = self.steps[step_num-1]
            # Yeni velocity değeri
            new_velocity = step.velocity + delta
            # Sınırlar içinde kal
            new_velocity = max(0, min(127, new_velocity))
            # Velocity değerini güncelle
            step.velocity = new_velocity
            
            # LED güncelleme için velocity değerlerini kaydet
            velocities[step_num] = new_velocity
        
        # LED yöneticisini güncelle
        if hasattr(self, 'ledManager') and self.ledManager:
            self.ledManager.setVelocities(velocities)
        
        # İlk seçili adımın velocity değerini döndür
        first_step = min(self.selectedSteps)
        velocity = self.getStepVelocity(first_step)
        print(f"Velocity: {velocity}")
        
        return velocity
    
    def setStepEnvelope(self, stepNumber, param, value):
        """Bir adımın envelope değerini ayarlar
        
        Args:
            stepNumber: Adım numarası (1-tabanlı)
            param: Envelope parametresi ('attack', 'decay', 'sustain', 'release')
            value: Yeni değer (attack, decay, release için ms, sustain için %)
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if 1 <= stepNumber <= self.totalSteps:
            step = self.steps[stepNumber-1]
            if param in ['attack', 'decay', 'sustain', 'release']:
                # Değer sınırlamaları
                if param == 'attack':
                    value = max(1, min(1000, value))  # 1-1000 ms
                elif param == 'decay':
                    value = max(1, min(2000, value))  # 1-2000 ms
                elif param == 'sustain':
                    value = max(0, min(100, value))   # 0-100 %
                elif param == 'release':
                    value = max(1, min(3000, value))  # 1-3000 ms
                
                step.envelope[param] = value
                print(f"Step {stepNumber} {param}: {value}")
                return True
        return False
    
    def getStepEnvelope(self, stepNumber):
        """Bir adımın envelope değerlerini döndürür
        
        Args:
            stepNumber: Adım numarası (1-tabanlı)
        
        Returns:
            dict: Envelope değerleri {'attack', 'decay', 'sustain', 'release'}
        """
        if 1 <= stepNumber <= self.totalSteps:
            return self.steps[stepNumber-1].envelope
        return None
    
    def adjustSelectedEnvelope(self, param, delta):
        """Seçili adımların envelope değerlerini değiştirir
        
        Args:
            param: Envelope parametresi ('attack', 'decay', 'sustain', 'release')
            delta: Değişim miktarı
            
        Returns:
            int: İlk seçili adımın yeni envelope değeri, veya hiç adım seçili değilse -1
        """
        if not self.selectedSteps:
            print("Hiçbir step seçili değil!")
            return -1
        
        for step_num in self.selectedSteps:
            step = self.steps[step_num-1]
            # Mevcut değeri al
            current_value = step.envelope[param]
            # Değişim faktörü (param'a göre değişir)
            factor = 1
            if param == 'attack':
                factor = 5
            elif param == 'decay':
                factor = 10
            elif param == 'sustain':
                factor = 1
            elif param == 'release':
                factor = 10
            
            # Yeni değer
            new_value = current_value + (delta * factor)
            
            # Değeri güncelle
            self.setStepEnvelope(step_num, param, new_value)
        
        # İlk seçili adımın envelope değerini döndür
        first_step = min(self.selectedSteps)
        env = self.getStepEnvelope(first_step)
        print(f"{param.capitalize()}: {env[param]}")
        
        return env[param]
    
    def transposeSteps(self, semitones):
        """Tüm adımları belirtilen yarım ton kadar transpoze eder
        
        Args:
            semitones: Transpoze miktarı (+ yukarı, - aşağı)
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        # Tüm adımlar için MIDI notalarını ve frekansları güncelle
        for step in self.steps:
            # MIDI notasını transpoze et
            old_midi = step.midiNote
            new_midi = max(0, min(127, old_midi + semitones))  # MIDI sınırları içinde kal
            step.midiNote = new_midi
            
            # Frekansı güncelle
            step.updateFrequencyFromMidi()
        
        print(f"Tüm adımlar {semitones} yarım ton transpoze edildi")
        return True