# features/playback.py
# Bu dosya, sequencer çalma kontrolü işlevlerini sağlar

class PlaybackManager:
    """Sequencer çalma kontrolü sınıfı"""
    
    def __init__(self, stepController, midiOutput):
        """PlaybackManager sınıfını başlat
        
        Args:
            stepController: StepController nesnesi
            midiOutput: MidiOutput nesnesi
        """
        self.stepController = stepController
        self.midiOutput = midiOutput
    
    def play(self):
        """Sequencer'ı başlat
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        return self.midiOutput.start()
    
    def pause(self):
        """Sequencer'ı duraklat
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        return self.midiOutput.pause()
    
    def stop(self):
        """Sequencer'ı durdur
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        return self.midiOutput.stop()
    
    def togglePlayPause(self):
        """Sequencer'ın çalma/duraklatma durumunu değiştirir
        
        Returns:
            bool: Sequencer çalıyorsa True, değilse False
        """
        if self.midiOutput.isRunning:
            self.midiOutput.pause()
            print("Sequencer duraklatıldı")
            return False
        else:
            self.midiOutput.start()
            print("Sequencer başlatıldı")
            return True
    
    def toggleRandomMode(self):
        """Rastgele çalma modunu açıp kapatır
        
        Returns:
            bool: Rastgele çalma modu açık ise True, değilse False
        """
        return self.midiOutput.toggleRandomPlayMode()
    
    def toggleFullRandomMode(self):
        """Tam rastgele çalma modunu açıp kapatır
        
        Returns:
            bool: Tam rastgele çalma modu açık ise True, değilse False
        """
        return self.midiOutput.toggleFullRandomMode()
    
    def resetRandomMode(self):
        """Rastgele modu normal sıralı moda döndürür
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        return self.midiOutput.resetRandomMode()
    
    def doubleTempo(self):
        """Tempoyu iki katına çıkarır
        
        Returns:
            float: Yeni tempo değeri
        """
        return self.midiOutput.doubleTime()
    
    def halfTempo(self):
        """Tempoyu yarıya indirir
        
        Returns:
            float: Yeni tempo değeri
        """
        return self.midiOutput.halfTime()
    
    def resetTempo(self):
        """Tempoyu orijinal değerine geri döndürür
        
        Returns:
            float: Orijinal tempo değeri
        """
        return self.midiOutput.resetTempo()
    
    def setTempo(self, bpm):
        """Tempo değerini ayarla
        
        Args:
            bpm: Beats per minute değeri (30-300)
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        return self.midiOutput.setTempo(bpm)
    
    def setGateTime(self, gateTime):
        """Gate time değerini ayarla (0.1-1.0 arası)
        
        Args:
            gateTime: Gate time değeri (0.1-1.0)
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        return self.midiOutput.setGateTime(gateTime)