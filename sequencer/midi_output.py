# sequencer/midi_output.py
# Bu dosya, MIDI mesajları üretme ve gönderme işlemlerini içerir

from machine import UART, Timer
import time
import config
from sequencer.utils import midiToFreq, getNoteName
import random

# Yardımcı fonksiyon - kendi shuffle fonksiyonumuzu tanımlayalım
def customShuffle(seq):
    """MicroPython için liste karıştırma fonksiyonu"""
    length = len(seq)
    for i in range(length - 1, 0, -1):
        # Rastgele bir indeks seç
        j = random.randint(0, i)
        # Elemanları değiştir
        seq[i], seq[j] = seq[j], seq[i]
    return seq

class MidiOutput:
    """MIDI mesajları gönderme ve sequencer zamanlama sınıfı"""
    
    def __init__(self, uartId=0, txPin=None, rxPin=None, baudrate=31250):
        """MidiOutput sınıfını başlat
        
        Args:
            uartId: UART arayüz ID'si
            txPin: TX pin numarası, None ise config'ten alınır
            rxPin: RX pin numarası, None ise config'ten alınır
            baudrate: UART baudrate değeri
        """
        # Pin numaralarını config'den al (eğer parametre olarak verilmemişse)
        if txPin is None:
            txPin = config.midiTxPin
        if rxPin is None:
            rxPin = config.midiRxPin
            
        # UART arayüzünü başlat
        self.uart = UART(uartId, baudrate=baudrate, tx=txPin, rx=rxPin)
        
        # Sequencer durumu
        self.isRunning = False
        self.isPaused = False
        self.currentStep = 0
        
        # Step controller referansı
        self.stepController = None
        
        # LED yöneticisi referansı
        self.ledManager = None
        
        # Tempo
        self.tempo = config.defaultTempo  # BPM
        self.originalTempo = self.tempo   # Tempo aşırtma için orijinal değer
        
        # 4'lük nota süresi (ms) - 60000ms / BPM
        self.quarterNoteMs = 60000 / self.tempo
        
        # Adım aralığı olarak 4'lük nota kullan
        self.stepInterval = self.quarterNoteMs  # ms
        
        # Gate time (nota çalma süresi)
        self.gateTime = config.defaultGateTime
        
        # Timerlar
        self.stepTimer = None
        self.gateTimer = None
        
        # Rastgele çalma modu
        self.randomPlayMode = False
        self.fullRandomMode = False
        
        # Adım sırası - normal modda sıralı, rastgele modda karıştırılmış
        self.stepSequence = list(range(config.defaultStepCount))
        
        # Aktif notalar
        self.activeNotes = []
        
        # Transpoze değeri
        self.transposeAmount = 0
        
        print(f"MIDI çıkışı başlatıldı: Tempo {self.tempo} BPM")
        print(f"4'lük nota süresi: {self.stepInterval:.2f} ms")
    
    def setLedManager(self, ledManager):
        """LED yöneticisini ayarla
        
        Args:
            ledManager: LEDManager nesnesi
        """
        self.ledManager = ledManager
    
    def shuffleStepSequence(self):
        """Adım sırasını karıştırır
        
        Returns:
            list: Karıştırılmış adım sırası
        """
        if self.stepController is None:
            return self.stepSequence
            
        # Toplam adım sayısı kadar liste oluştur ve karıştır
        total_steps = self.stepController.totalSteps
        self.stepSequence = list(range(total_steps))
        
        # customShuffle fonksiyonunu kullan
        customShuffle(self.stepSequence)
        
        print(f"Adım sırası karıştırıldı: {self.stepSequence}")
        return self.stepSequence
    
    def resetStepSequence(self):
        """Adım sırasını normal haline döndürür
        
        Returns:
            list: Normal sıralı adım dizisi
        """
        if self.stepController is None:
            return self.stepSequence
            
        # Toplam adım sayısına göre normal sıra oluştur
        total_steps = self.stepController.totalSteps
        self.stepSequence = list(range(total_steps))
        
        print("Adım sırası normal hale getirildi")
        return self.stepSequence
    
    def _stepTimerCallback(self, timer):
        """Step timer için callback fonksiyonu - Solo ve Mute desteği ile"""
        if not self.isRunning or self.stepController is None:
            return
            
        # Tüm aktif notaları kapat
        self.allNotesOff()
        
        try:
            # Sonraki adıma geç (çalma modu seçimine göre)
            if self.fullRandomMode:
                # Tam rastgele mod - Her seferinde yeni rastgele adım
                self.currentStep = random.randint(0, self.stepController.totalSteps - 1)
                print(f"Tam rastgele adım: {self.currentStep + 1}")
            elif self.randomPlayMode and self.stepSequence:
                # Rastgele sıra modu - Önceden karıştırılmış sıra
                try:
                    current_sequence_index = self.stepSequence.index(self.currentStep)
                    # Sonraki indeksi hesapla
                    next_sequence_index = (current_sequence_index + 1) % len(self.stepSequence)
                    self.currentStep = self.stepSequence[next_sequence_index]
                except ValueError:
                    # Eğer mevcut adım dizide bulunamazsa, ilk adımdan başla
                    self.currentStep = self.stepSequence[0] if self.stepSequence else 0
                except Exception as e:
                    # Herhangi bir hata durumunda normal moda dön
                    print(f"Rastgele mod hatası: {e}, normal moda dönülüyor")
                    self.randomPlayMode = False
                    self.currentStep = (self.currentStep + 1) % self.stepController.totalSteps
            else:
                # Normal sıralı mod
                self.currentStep = (self.currentStep + 1) % self.stepController.totalSteps
            
            # Adımın çalınabilir olup olmadığını kontrol et
            step_audible = True
            current_step_1based = self.currentStep + 1  # 1-tabanlı step numarası
            
            # Mute/Solo kontrolü
            if hasattr(self.stepController, 'isStepAudible'):
                step_audible = self.stepController.isStepAudible(current_step_1based)
            
            # LED yöneticisi mevcutsa, mevcut adımı güncelle
            if self.ledManager:
                self.ledManager.setCurrentStep(self.currentStep)
            
            # Adım çalınabilirse notayı çal
            if step_audible:
                # Sıradaki notayı çal
                step = self.stepController.steps[self.currentStep]
                next_note = step.midiNote
                
                # Velocity değerini al
                velocity = step.velocity
                
                # Transpoze miktarını uygula
                if self.transposeAmount != 0:
                    # MIDI nota sınırları içinde kalmak için
                    next_note = max(0, min(127, next_note + self.transposeAmount))
                
                # Notayı çal
                self.noteOn(0, next_note, velocity)
                
                # Debug
                mode_str = "TAM RASTGELE" if self.fullRandomMode else "RASTGELE" if self.randomPlayMode else "SIRALI"
                print(f"\n--- ADIM {self.currentStep + 1}/{self.stepController.totalSteps} ({mode_str}) ÇALINIYOR --- Nota: {next_note}, Velocity: {velocity}")
            else:
                # Adım çalınabilir değil (mute veya solo nedeniyle)
                mode_str = "TAM RASTGELE" if self.fullRandomMode else "RASTGELE" if self.randomPlayMode else "SIRALI"
                print(f"\n--- ADIM {self.currentStep + 1}/{self.stepController.totalSteps} ({mode_str}) SESSİZ ---")
        except Exception as e:
            # Herhangi bir hata durumunda güvenli modda devam et
            print(f"Step timer hatası: {e}")
            # Herhangi bir hata durumunda normal moda dön
            self.fullRandomMode = False
            self.randomPlayMode = False
            self.currentStep = (self.currentStep + 1) % self.stepController.totalSteps
            
    def sendMidiMessage(self, message):
        """MIDI mesajı gönder
        
        Args:
            message: MIDI mesaj verisi (bytes veya bytearray)
        """
        # Mesajı doğrudan gönder
        self.uart.write(message)
    
    def noteOn(self, channel, note, velocity=None):
        """MIDI Note On mesajı gönder (velocity desteği ile)
        
        Args:
            channel: MIDI kanalı (0-15)
            note: MIDI nota numarası (0-127)
            velocity: Velocity değeri (0-127), None ise varsayılan değer kullanılır
        """
        # Velocity parametresi verilmemişse, step_controller'dan al veya varsayılanı kullan
        if velocity is None:
            if self.stepController and 0 <= self.currentStep < len(self.stepController.steps):
                velocity = self.stepController.steps[self.currentStep].velocity
            else:
                velocity = 100  # Varsayılan
        
        # Sınır kontrolü
        if not (0 <= channel <= 15 and 0 <= note <= 127 and 0 <= velocity <= 127):
            return
            
        # Note On mesajı
        message = bytearray([0x90 | channel, note, velocity])
        self.sendMidiMessage(message)
        
        # Aktif nota listesine ekle
        if note not in self.activeNotes:
            self.activeNotes.append(note)
        
        # Debug
        print(f"Note On: {note} ({getNoteName(note)}), velocity: {velocity}")
        
        # Gate timer'ı başlat
        self._startGateTimer()
        
        # ADSR değerleri uygulama (şu an için sadece debug amaçlı)
        if self.stepController and 0 <= self.currentStep < len(self.stepController.steps):
            envelope = self.stepController.steps[self.currentStep].envelope
            print(f"ADSR: A={envelope['attack']}ms, D={envelope['decay']}ms, S={envelope['sustain']}%, R={envelope['release']}ms")
    
    def noteOff(self, channel, note, velocity=0):
        """MIDI Note Off mesajı gönder
        
        Args:
            channel: MIDI kanalı (0-15)
            note: MIDI nota numarası (0-127)
            velocity: Release velocity değeri (genellikle 0)
        """
        # Sınır kontrolü
        if not (0 <= channel <= 15 and 0 <= note <= 127 and 0 <= velocity <= 127):
            return
            
        # Note Off mesajı
        message = bytearray([0x80 | channel, note, velocity])
        self.sendMidiMessage(message)
        
        # Aktif nota listesinden çıkar
        if note in self.activeNotes:
            self.activeNotes.remove(note)
        
        # Debug
        print(f"Note Off: {note} ({getNoteName(note)})")
    
    def allNotesOff(self, channel=0):
        """Tüm notaları kapat
        
        Args:
            channel: MIDI kanalı (0-15)
        """
        # Active notaları tek tek kapat
        for note in self.activeNotes.copy():
            self.noteOff(channel, note)
        
        # All Notes Off CC mesajı
        message = bytearray([0xB0 | channel, 123, 0])
        self.sendMidiMessage(message)
        
        # Aktif nota listesini temizle
        self.activeNotes = []
    
    # sequencer/midi_output.py içinde setTempo metodunu güncelleyelim
    def setTempo(self, bpm):
        """Tempo değerini ayarla
        
        Args:
            bpm: Beats per minute değeri (30-300)
                
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if 30 <= bpm <= 300:
            self.tempo = bpm
            
            # 4'lük nota süresi (ms)
            self.quarterNoteMs = 60000 / self.tempo
            
            # Adım aralığını 4'lük nota olarak ayarla
            self.stepInterval = self.quarterNoteMs
            
            # Eğer step timer çalışıyorsa, timer'ı yeniden başlatmadan sadece interval'i güncelle
            if self.isRunning and self.stepTimer:
                # Mevcut timer'ı durdurmadan interval'i güncelle
                # Bu, bir sonraki adımda yeni tempo ile çalmaya devam etmesini sağlar
                self.stepTimer.deinit()
                self.stepTimer = Timer(-1)
                self.stepTimer.init(period=int(self.stepInterval), mode=Timer.PERIODIC, 
                                  callback=self._stepTimerCallback)
                    
            print(f"Tempo ayarlandı: {self.tempo} BPM (4'lük nota aralığı: {self.stepInterval:.2f} ms)")
            return True
        return False
    
    def setGateTime(self, gateTime):
        """Gate time değerini ayarla (0.1-1.0 arası)
        
        Args:
            gateTime: Gate time değeri (0.1-1.0)
            
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if 0.1 <= gateTime <= 1.0:
            self.gateTime = gateTime
            print(f"Gate time ayarlandı: %{int(self.gateTime * 100)}")
            return True
        return False
    
    def _gateTimerCallback(self, timer):
        """Gate timer için callback fonksiyonu"""
        if not self.isRunning:
            return
            
        # Gate time sonunda notaları kapat
        self.allNotesOff()
    
    def _startStepTimer(self):
        """Adım timerını başlat"""
        if self.stepTimer:
            self.stepTimer.deinit()
            
        self.stepTimer = Timer(-1)
        self.stepTimer.init(period=int(self.stepInterval), mode=Timer.PERIODIC, 
                           callback=self._stepTimerCallback)
    
    def _restartStepTimer(self):
        """Adım timerını yeniden başlat"""
        if self.stepTimer:
            self.stepTimer.deinit()
        self._startStepTimer()
    
    def _startGateTimer(self):
        """Gate timerını başlat"""
        # Gate time 1.0 ise (tam uzunluktaysa) timer kurma
        if self.gateTime >= 1.0:
            return
            
        # Gate timerı durdur (eğer çalışıyorsa)
        if self.gateTimer:
            self.gateTimer.deinit()
            
        # Yeni gate timerı başlat
        gate_ms = int(self.stepInterval * self.gateTime)
        self.gateTimer = Timer(-1)
        self.gateTimer.init(period=gate_ms, mode=Timer.ONE_SHOT, 
                           callback=self._gateTimerCallback)
    
    def start(self):
        """Sequencer'ı başlat
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        self.allNotesOff()  # Temiz başlangıç
        
        if self.isPaused:
            # Duraklatılmış durumdan devam et
            self.isRunning = True
            self.isPaused = False
            self._startStepTimer()
            print(f"Sequencer duraklama sonrası devam ediyor (adım: {self.currentStep + 1})")
            return True
        
        # İlk adımı belirle
        if self.randomPlayMode and self.stepSequence:
            # Rastgele modda ilk adımı dizinin ilk elemanı olarak ayarla
            self.currentStep = self.stepSequence[0]
            print(f"Rastgele mod, başlangıç adımı: {self.currentStep+1}")
        else:
            # Normal modda 0. adımdan başla
            self.currentStep = 0
            print(f"Normal mod, başlangıç adımı: {self.currentStep+1}")
        
        self.isRunning = True
        self._startStepTimer()
        
        # Başlangıç notasını hemen çal (ilk adım için beklemeden)
        if self.stepController and self.currentStep < len(self.stepController.steps):
            step = self.stepController.steps[self.currentStep]
            next_note = step.midiNote
            velocity = step.velocity
            
            # Transpoze miktarını uygula
            if self.transposeAmount != 0:
                next_note = max(0, min(127, next_note + self.transposeAmount))
                
            self.noteOn(0, next_note, velocity)
        
        # Bilgi mesajı
        mode_str = "tam rastgele" if self.fullRandomMode else "rastgele sırada" if self.randomPlayMode else "normal sırada"
        print(f"Sequencer başlatıldı ({mode_str})")
        return True
    
    def pause(self):
        """Sequencer'ı duraklat
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        if self.isRunning:
            self.isRunning = False
            self.isPaused = True
            
            # Timer'ları durdur
            if self.stepTimer:
                self.stepTimer.deinit()
            if self.gateTimer:
                self.gateTimer.deinit()
                
            self.allNotesOff()
            print(f"Sequencer duraklatıldı (adım: {self.currentStep + 1})")
            return True
        return False
    
    def stop(self):
        """Sequencer'ı durdur ve sıfırla
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        self.isRunning = False
        self.isPaused = False
        
        # Timer'ları durdur
        if self.stepTimer:
            self.stepTimer.deinit()
        if self.gateTimer:
            self.gateTimer.deinit()
            
        self.allNotesOff()
        self.currentStep = 0
        print("Sequencer durduruldu ve sıfırlandı")
        return True
    
    def updateSequencer(self, stepController):
        """Step controller referansını günceller
        
        Args:
            stepController: StepController nesnesi
        """
        # Step controller'ı sakla
        self.stepController = stepController
        
        # Eğer step controller'da ledManager yoksa ve bu sınıfta varsa, ata
        if self.stepController and not self.stepController.ledManager and self.ledManager:
            self.stepController.setLedManager(self.ledManager)
    
    def toggleRandomPlayMode(self):
        """Rastgele çalma modunu açar/kapatır
        
        Returns:
            bool: Rastgele çalma modu açık ise True, değilse False
        """
        # Tam rastgele modu kapat (eğer aktifse)
        self.fullRandomMode = False
        
        # Rastgele modu değiştir
        self.randomPlayMode = not self.randomPlayMode
        
        if self.randomPlayMode:
            # Yeni sıralama üret
            self.shuffleStepSequence()
            print("Rastgele çalma modu: AÇIK")
        else:
            # Normal sıraya dön
            self.resetStepSequence()
            print("Rastgele çalma modu: KAPALI")
        
        return self.randomPlayMode
    
    def toggleFullRandomMode(self):
        """Tam rastgele çalma modunu açıp kapatır (her adımda yeni rastgele)
        
        Returns:
            bool: Tam rastgele çalma modu açık ise True, değilse False
        """
        # Normal rastgele modu kapat
        self.randomPlayMode = False
        
        # Tam rastgele modu değiştir
        self.fullRandomMode = not self.fullRandomMode
        
        if self.fullRandomMode:
            print("TAM rastgele çalma modu: AÇIK (her adım rastgele seçilecek)")
        else:
            print("TAM rastgele çalma modu: KAPALI")
            # Normal sıralı moda geri dön
            self.resetStepSequence()
        
        return self.fullRandomMode
    
    def resetRandomMode(self):
        """Rastgele modu normal sıralı moda döndürür
        
        Returns:
            bool: İşlem başarılıysa True, değilse False
        """
        # Tüm rastgele modları kapat
        self.randomPlayMode = False
        self.fullRandomMode = False
        
        # Normal sıralı moda dön
        self.resetStepSequence()
        print("Rastgele mod kapatıldı - Normal sıralı mod aktif")
        return True
    
    def doubleTime(self):
        """Tempoyu iki katına çıkarır
        
        Returns:
            float: Yeni tempo değeri
        """
        # Orijinal tempoyu sakla (eğer daha önce kaydedilmemişse)
        if not hasattr(self, 'originalTempo'):
            self.originalTempo = self.tempo
        
        # Tempoyu iki katına çıkar
        new_tempo = self.tempo * 2
        
        # Tempo sınırları içinde kal
        if 30 <= new_tempo <= 300:
            self.setTempo(new_tempo)
            print(f"Tempo iki katına çıkarıldı: {new_tempo} BPM")
        else:
            new_tempo = 300  # Maximum tempo
            self.setTempo(new_tempo)
            print(f"Tempo maximum değere ayarlandı: {new_tempo} BPM")
            
        return new_tempo
    
    def halfTime(self):
        """Tempoyu yarıya indirir
        
        Returns:
            float: Yeni tempo değeri
        """
        # Orijinal tempoyu sakla (eğer daha önce kaydedilmemişse)
        if not hasattr(self, 'originalTempo'):
            self.originalTempo = self.tempo
        
        # Tempoyu yarıya indir
        new_tempo = self.tempo / 2
        
        # Tempo sınırları içinde kal
        if 30 <= new_tempo <= 300:
            self.setTempo(new_tempo)
            print(f"Tempo yarıya indirildi: {new_tempo} BPM")
        else:
            new_tempo = 30  # Minimum tempo
            self.setTempo(new_tempo)
            print(f"Tempo minimum değere ayarlandı: {new_tempo} BPM")
            
        return new_tempo
    
    def resetTempo(self):
        """Tempoyu orijinal değerine geri döndürür
        
        Returns:
            float: Orijinal tempo değeri
        """
        if hasattr(self, 'originalTempo'):
            self.setTempo(self.originalTempo)
            print(f"Tempo orijinal değerine döndürüldü: {self.originalTempo} BPM")
            return self.originalTempo
        return self.tempo
    
    def setTransposeAmount(self, semitones):
        """Transpoze miktarını ayarlar
        
        Args:
            semitones: Yarım ton sayısı (-24 ile +24 arası)
            
        Returns:
            int: Transpoze miktarı
        """
        # Transpoze miktarını sınırla (-24 ile +24 arası)
        self.transposeAmount = max(-24, min(24, semitones))
        print(f"Transpoze miktarı: {self.transposeAmount} yarım ton")
        return self.transposeAmount