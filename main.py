# main.py - Düzeltilmiş Versiyon
# Bu dosya, uygulamayı başlatan ve tüm bileşenleri bir araya getiren ana dosyadır
# Raspberry Pi Pico açıldığında otomatik olarak çalıştırılır

import time
import gc
import config

def initializeSystem():
    """Sistemi başlatır ve tüm alt sistemleri oluşturur"""
    print("\n*** BABI Sequencer v" + config.appVersion + " Başlatılıyor ***\n")
     
    # Bellek kullanımı bilgisini göster
    gc.collect()  # Garbage collection'ı çalıştır
    mem_free = gc.mem_free()
    mem_alloc = gc.mem_alloc()
    total_mem = mem_free + mem_alloc
    
    print(f"Bellek Durumu:")
    print(f"Serbest Bellek: {mem_free / 1024:.2f} KB")
    print(f"Toplam Bellek: {total_mem / 1024:.2f} KB")
    print(f"Kullanım Oranı: {(mem_alloc / total_mem) * 100:.2f}%")
    
    # Mods dizinini oluştur
    try:
        import os
        if config.ModsDir not in os.listdir('/'):
            os.mkdir(config.ModsDir)
            print(f"Mods dizini oluşturuldu: {config.ModsDir}")
    except Exception as e:
        print(f"Mods dizini oluşturulamadı: {e}")
    
    # Hardware bileşenlerini başlat
    try:
        from hardware.buttons import ButtonManager
        from hardware.encoders import EncoderManager
        from hardware.leds import LEDManager
        
        print("\nDonanım bileşenleri başlatılıyor...")
        buttonManager = ButtonManager()
        encoderManager = EncoderManager()
        ledManager = LEDManager()
        
        print("Donanım bileşenleri başlatıldı")
    except Exception as e:
        print(f"Donanım bileşenleri başlatılamadı: {e}")
        import sys
        sys.print_exception(e)
        return None, None
    
    try:
        from hardware.display import DisplayManager
        print("\nEkran yöneticisi başlatılıyor...")
        displayManager = DisplayManager()
        print("Ekran yöneticisi başlatıldı")
    except Exception as e:
        print(f"Ekran yöneticisi başlatılamadı: {e}")
        import sys
        sys.print_exception(e)
        displayManager = None
    
    # Sequencer bileşenlerini başlat
    try:
        from sequencer.step_controller import StepController
        from sequencer.midi_output import MidiOutput
        from sequencer.pattern_manager import PatternManager
        
        print("\nSequencer bileşenleri başlatılıyor...")
        stepController = StepController()
        midiOutput = MidiOutput()
        patternManager = PatternManager(stepController)
        
        # MidiOutput'a StepController'ı bağla
        midiOutput.updateSequencer(stepController)
        
        # LED yöneticisini StepController'a bağla
        stepController.setLedManager(ledManager)
        
        # LED yöneticisini MidiOutput'a bağla
        midiOutput.setLedManager(ledManager)
        
        print("Sequencer bileşenleri başlatıldı")
    except Exception as e:
        print(f"Sequencer bileşenleri başlatılamadı: {e}")
        import sys
        sys.print_exception(e)
        return None, None
    
    # Feature bileşenlerini başlat
    try:
        from features.step_config import StepConfiguration
        from features.playback import PlaybackManager
        from features.envelope import EnvelopeManager
        from features.transpose import TransposeManager
        from features.random_modes import RandomModeManager
        
        print("\nFeature bileşenleri başlatılıyor...")
        stepConfig = StepConfiguration(stepController)
        playbackManager = PlaybackManager(stepController, midiOutput)
        envelopeManager = EnvelopeManager(stepController)
        transposeManager = TransposeManager(stepController, midiOutput)
        randomModeManager = RandomModeManager(midiOutput)
        
        print("Feature bileşenleri başlatıldı")
    except Exception as e:
        print(f"Feature bileşenleri başlatılamadı: {e}")
        import sys
        sys.print_exception(e)
        return None, None
    
    # UI bileşenlerini başlat (eğer displayManager varsa)
    uiManager = None
    if displayManager:
        try:
            from ui.ui_manager import UIManager
            from ui.input_handler import InputHandler
            
            print("\nUI bileşenleri başlatılıyor...")
            uiManager = UIManager(displayManager)
            
            # UI yöneticisine sequencer bileşenlerini tanıt
            uiManager.setSystemComponents(stepController, midiOutput)
            
            inputHandler = InputHandler(
                buttonManager,
                encoderManager,
                stepController,
                midiOutput,
                playbackManager,
                stepConfig,
                envelopeManager,
                transposeManager,
                randomModeManager,
                uiManager
            )
            
            print("UI bileşenleri başlatıldı")
        except Exception as e:
            print(f"UI bileşenleri başlatılamadı: {e}")
            import sys
            sys.print_exception(e)
            uiManager = None
    
    # Tüm bileşenleri tek bir sınıfta birleştir
    class SequencerSystem:
        def __init__(self):
            # Hardware
            self.buttonManager = buttonManager
            self.encoderManager = encoderManager
            self.ledManager = ledManager
            self.displayManager = displayManager
            
            # Sequencer
            self.stepController = stepController
            self.midiOutput = midiOutput
            self.patternManager = patternManager
            
            # Features
            self.stepConfig = stepConfig
            self.playbackManager = playbackManager
            self.envelopeManager = envelopeManager
            self.transposeManager = transposeManager
            self.randomModeManager = randomModeManager
            
            # UI
            self.uiManager = uiManager
            self.inputHandler = inputHandler if displayManager else None
            
            # Durum değişkenleri
            self.isRunning = False
            self.currentMode = "normal"  # normal, menu, envelope, velocity, transpose, etc.
    
    sequencerSystem = SequencerSystem()
    
    # Temel başlangıç işlevlerini çağır
    if sequencerSystem.displayManager:
        sequencerSystem.displayManager.showStartupScreen()
    
    # Başlangıç ekranını 2 saniye göster
    time.sleep(2)
    
    print("\n*** Sistem başlatıldı, uygulama hazır ***\n")
    
    return sequencerSystem, runMainLoop

def runMainLoop(system):
    """Ana uygulama döngüsünü çalıştırır
    
    Args:
        system: SequencerSystem nesnesi
    """
    print("Ana uygulama döngüsü başlatılıyor...")
    system.isRunning = True
    
    try:
        # UI kullanılıyorsa
        if system.uiManager and system.inputHandler:
            print("UI ve input handler modunu kullanarak çalışıyor")
            # Ana ekranı göster
            system.uiManager.showMainScreen()
            
            # Ana döngü
            while system.isRunning:
                try:
                    # Kullanıcı girişlerini işle
                    system.inputHandler.processButtons()
                    system.inputHandler.processEncoder()
                    
                    # Sequencer'ı güncelle
                    system.midiOutput.updateSequencer(system.stepController)
                    
                    # Ekranı güncelle (belirli aralıklarla)
                    current_time = time.ticks_ms()
                    if not hasattr(system, 'last_display_update') or time.ticks_diff(current_time, system.last_display_update) > config.displayUpdateInterval:
                        system.uiManager.update()
                        system.last_display_update = current_time
                    
                    # Kısa bir bekleme (CPU kullanımını azaltmak için)
                    time.sleep(0.01)
                except Exception as e:
                    print(f"Ana döngü hatası: {e}")
                    import sys
                    sys.print_exception(e)
        else:
            # UI olmadan basit mod
            print("Basit mod kullanarak çalışıyor (UI olmadan)")
            # Ana döngü
            while system.isRunning:
                try:
                    # Butonları işle
                    pressed_buttons = system.buttonManager.getPressedButtons()
                    if pressed_buttons:
                        print(f"Basılı butonlar: {pressed_buttons}")
                        
                        # Play/Pause butonu (buton 20)
                        if 20 in pressed_buttons:
                            system.playbackManager.togglePlayPause()
                        
                        # Stop butonu (buton 21)
                        elif 21 in pressed_buttons:
                            system.playbackManager.stop()
                        
                        # Adım butonları (buton 1-16)
                        elif any(1 <= b <= 16 for b in pressed_buttons):
                            for b in [b for b in pressed_buttons if 1 <= b <= 16]:
                                # Shift butonu basılı mı? (buton 24)
                                shift_pressed = 24 in pressed_buttons
                                system.stepController.selectStep(b, not shift_pressed)
                    
                    # Encoder'ı işle
                    position_change = system.encoderManager.update()
                    if position_change != 0:
                        # Seçili adımlar varsa, onların değerlerini değiştir
                        if system.stepController.selectedSteps:
                            system.stepController.adjustValue(position_change)
                        else:
                            # Seçili adım yoksa, tempo değerini değiştir
                            current_tempo = system.midiOutput.tempo
                            new_tempo = max(30, min(300, current_tempo + position_change))
                            system.midiOutput.setTempo(new_tempo)
                    
                    # Encoder butonunu kontrol et
                    if system.encoderManager.checkButton():
                        # Tüm adımları seç/seçimini kaldır
                        system.stepController.toggleSelectionWithEncoderSwitch()
                    
                    # Sequencer'ı güncelle
                    system.midiOutput.updateSequencer(system.stepController)
                    
                    # Kısa bir bekleme
                    time.sleep(0.01)
                except Exception as e:
                    print(f"Ana döngü hatası: {e}")
                    import sys
                    sys.print_exception(e)
    except KeyboardInterrupt:
        print("Kullanıcı tarafından durduruldu")
    finally:
        # Temizleme işlemleri
        system.midiOutput.allNotesOff()
        system.isRunning = False
        print("Uygulama kapatıldı")

def main():
    """Ana program fonksiyonu"""
    try:
        # Sistemi başlat
        system, runLoop = initializeSystem()
        
        if system and runLoop:
            # Ana döngüyü çalıştır
            runLoop(system)
        else:
            print("Sistem başlatılamadı")
    except Exception as e:
        print(f"Ana program hatası: {e}")
        import sys
        sys.print_exception(e)

# Programı başlat
if __name__ == "__main__":
    main()