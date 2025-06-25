# Kurulum Kılavuzu / Installation Guide

Bu dokümant BABI SEQ projesinin detaylı kurulum talimatlarını içerir.

## 📋 Gereksinimler

### Donanım Gereksinimleri

#### Ana Bileşenler
| Bileşen | Model/Tip | Miktar | Açıklama |
|---------|-----------|--------|----------|
| Microcontroller | Raspberry Pi Pico (RP2040) | 1 | Ana işlemci |
| TFT Display | ILI9341 240x320 | 1 | Ana ekran |
| Touch Controller | XPT2046 | 1 | Dokunmatik kontrol |
| DAC | MCP4822 12-bit | 1 | CV çıkışı |
| Shift Register | 74HC165 | 4 | Buton matrisi |
| Encoder | Rotary Encoder | 1 | Parametre kontrolü |
| LED Strip | WS2812B | 1 (16 LED) | Görsel geri bildirim |

#### Destekleyici Bileşenler
- **Dirençler**: 10kΩ (20 adet), 1kΩ (8 adet), 330Ω (16 adet)
- **Kondansatörler**: 100nF (10 adet), 10µF (4 adet)
- **Transistörler**: 2N2222 (1 adet) - Gate çıkışı için
- **MIDI Konnektör**: DIN-5 (1 adet)
- **Optocoupler**: 6N138 (1 adet) - MIDI izolasyon

### Yazılım Gereksinimleri

#### Geliştirme Ortamı
- **MicroPython**: v1.20.0 veya üstü
- **IDE**: Thonny v4.0+ (önerilen) veya VS Code + MicroPython Extension
- **File Transfer Tool**: ampy, mpremote veya Thonny file manager

#### Bağımlılıklar
- MicroPython yerleşik modülleri (machine, time, json, math, random, gc, os)
- Özel sürücüler (lib/ klasöründe mevcut)

## 🔧 Hardware Kurulumu

### 1. Raspberry Pi Pico Hazırlığı

#### MicroPython Firmware Yükleme
```bash
# 1. Pi Pico'yu BOOTSEL tuşuna basarak bilgisayara bağlayın
# 2. RPI-RP2 sürücüsü olarak tanınmasını bekleyin
# 3. MicroPython firmware dosyasını indirin:
```

**Firmware İndirme**: [MicroPython Downloads](https://micropython.org/download/rp2-pico/)

```bash
# 4. .uf2 dosyasını RPI-RP2 sürücüsüne kopyalayın
# 5. Pico otomatik olarak yeniden başlayacak
```

#### İlk Test
```python
# Thonny ile bağlanıp test edin:
print("Hello, BABI SEQ!")
import machine
print(f"Unique ID: {machine.unique_id()}")
```

### 2. Pin Bağlantı Şeması

#### MIDI Çıkışı
```
Pico Pin → Bağlantı
────────────────────
GPIO 0   → MIDI TX (DIN-5 pin 5, 6N138 üzerinden)
GPIO 1   → MIDI RX (DIN-5 pin 4, opsiyonel)
```

#### TFT Ekran (SPI0)
```
Pico Pin → ILI9341 Pin
─────────────────────
GPIO 2   → RESET
GPIO 3   → DC (Data/Command)
GPIO 4   → MISO (Backlight kontrol, 3.3V'ye bağlı)
GPIO 5   → CS (Chip Select)
GPIO 6   → SCK (SPI Clock)
GPIO 7   → MOSI (SPI Data)
3.3V     → VCC
GND      → GND
```

#### Dokunmatik Ekran (XPT2046)
```
Pico Pin → XPT2046 Pin
─────────────────────
GPIO 8   → T_CS
GPIO 9   → T_CLK
GPIO 10  → T_DIN
GPIO 11  → T_DO
GPIO 12  → T_IRQ
```

#### CV Çıkışı (SPI1)
```
Pico Pin → MCP4822 Pin
─────────────────────
GPIO 13  → CS (Chip Select)
GPIO 21  → Gate Out (2N2222 transistör base)
GPIO 26  → SCK (SPI1 Clock)
GPIO 27  → SDI (SPI1 Data)
```

**MCP4822 Bağlantısı**:
```
MCP4822 Pin → Bağlantı
────────────────────
1 (VDD)     → 3.3V
2 (CS)      → GPIO 13
3 (SCK)     → GPIO 26
4 (SDI)     → GPIO 27
5 (LDAC)    → GND
6 (SHDN)    → 3.3V
7 (VSS)     → GND
8 (VOUTB)   → CV Out B (Velocity)
9 (VREFB)   → 3.3V (veya harici referans)
10 (AVSS)   → GND
11 (VREFD)  → 3.3V (veya harici referans)
12 (VOUTA)  → CV Out A (Pitch)
```

#### Kontroller
```
Pico Pin → Bağlantı
─────────────────────
GPIO 15  → Encoder CLK
GPIO 16  → Encoder DT
GPIO 17  → Encoder SW
GPIO 18  → 74HC165 Q7 (Serial Data Out)
GPIO 19  → 74HC165 CLK (Clock)
GPIO 20  → 74HC165 SH/LD (Shift/Load)
GPIO 22  → WS2812B Data In
```

#### 74HC165 Shift Register Zinciri
```
HC165 #1 Pin → Bağlantı
─────────────────────
1 (SH/LD)    → GPIO 20 (tüm HC165'ler paralel)
2 (CLK)      → GPIO 19 (tüm HC165'ler paralel)
7 (A-H)      → Buton 1-8 (pull-up dirençlerle)
9 (Q7)       → HC165 #2 Pin 10 (SER)
10 (SER)     → 3.3V (ilk chip için)
13 (Q7)      → GPIO 18 (son chip'den)
```

### 3. Güç Beslemesi

#### Güç Tüketimi Hesaplaması
```
Bileşen          Akım     Voltaj
─────────────────────────────────
Pico RP2040      ~100mA   3.3V
ILI9341 TFT      ~150mA   3.3V
LED Strip (16)   ~960mA   5V (60mA/LED)
Diğer IC'ler     ~50mA    3.3V
─────────────────────────────────
Toplam 3.3V      ~300mA
Toplam 5V        ~960mA
```

#### Önerilen Güç Kaynağı
- **5V/2A Adaptör** (USB veya DC)
- **LM1117-3.3 Regülatör** (5V'tan 3.3V'a çevrim)
- **Filtreleme Kondansatörleri**: 470µF (5V), 220µF (3.3V)

## 💻 Yazılım Kurulumu

### 1. Geliştirme Ortamı Hazırlığı

#### Thonny IDE Kurulumu
```bash
# Windows/Mac/Linux için:
# https://thonny.org adresinden indirin ve kurun

# Python ile kurulum:
pip install thonny
```

#### VS Code Alternatifi
```bash
# VS Code + MicroPython eklentisi
# 1. VS Code'u yükleyin
# 2. MicroPython eklentisini yükleyin
# 3. Pico'yu bağlayın ve tanıyın
```

### 2. Proje Dosyalarını İndirme

```bash
# GitHub'dan klonlama
git clone https://github.com/kullanici-adi/babi-seq.git
cd babi-seq

# Veya ZIP olarak indirme
# GitHub > Code > Download ZIP
```

### 3. Dosya Yükleme

#### Thonny ile Yükleme
```python
# 1. Thonny'yi açın
# 2. Run > Select interpreter > MicroPython (Raspberry Pi Pico)
# 3. File > Save as > MicroPython device
# 4. Tüm dosyaları tek tek yükleyin

# Klasör yapısını koru:
/main.py
/config.py
/features/
/hardware/
/sequencer/
/ui/
/lib/
/fonts/
/mods/
```

#### mpremote ile Yükleme
```bash
# mpremote kurulumu
pip install mpremote

# Dosya kopyalama
mpremote fs cp main.py :
mpremote fs cp config.py :
mpremote fs cp -r features/ :
mpremote fs cp -r hardware/ :
mpremote fs cp -r sequencer/ :
mpremote fs cp -r ui/ :
mpremote fs cp -r lib/ :
mpremote fs cp -r fonts/ :
mpremote fs cp -r mods/ :

# Dizin kontrolü
mpremote fs ls
```

#### Dosya Yapısı Kontrolü
```python
# Pico'da çalıştırın:
import os

def list_files(path="", prefix=""):
    """Dosya yapısını listele"""
    for file in os.listdir(path):
        full_path = f"{path}/{file}" if path else file
        print(f"{prefix}{file}")
        try:
            list_files(full_path, prefix + "  ")
        except OSError:
            pass  # Dosya (dizin değil)

list_files()
```

### 4. Konfigürasyon Ayarları

#### config.py Düzenleme
```python
# Pin numaralarını donanımınıza göre ayarlayın
midiTxPin = 0
midiRxPin = 1

# TFT pinleri
tftCs = 5
tftSck = 6
tftMosi = 7
tftDc = 3
tftRst = 2

# CV pinleri
cvCs = 13
cvSck = 26
cvMosi = 27
cvGate = 21

# Diğer ayarları ihtiyacınıza göre değiştirin
defaultTempo = 120
defaultGateTime = 0.5
```

### 5. İlk Çalıştırma

#### Manuel Başlatma
```python
# Thonny REPL'de:
import main
main.main()
```

#### Otomatik Başlatma
```python
# main.py dosyasının sonuna ekleyin:
if __name__ == "__main__":
    main()
```

#### Sistem Testi
```python
# Test scripti çalıştırın:
import tests.system_test
tests.system_test.run_all_tests()
```

## 🧪 Test ve Doğrulama

### 1. Hardware Testleri

#### Pin Connectivity Test
```python
# Pin test scripti
from machine import Pin
import time

def test_pins():
    """Tüm pinleri test et"""
    pins = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 26, 27]
    
    for pin_num in pins:
        try:
            pin = Pin(pin_num, Pin.OUT)
            pin.on()
            time.sleep(0.1)
            pin.off()
            print(f"✅ GPIO {pin_num} OK")
        except Exception as e:
            print(f"❌ GPIO {pin_num} HATA: {e}")

test_pins()
```

#### TFT Display Test
```python
# TFT test
from hardware.display import DisplayManager

try:
    display = DisplayManager()
    display.clear()
    display.drawText(10, 10, "BABI SEQ Test")
    print("✅ TFT Display OK")
except Exception as e:
    print(f"❌ TFT Display HATA: {e}")
```

#### MIDI Test
```python
# MIDI çıkış testi
from sequencer.midi_output import MidiOutput

try:
    midi = MidiOutput()
    midi.noteOn(0, 60, 100)  # C4 nota
    time.sleep(0.5)
    midi.noteOff(0, 60)
    print("✅ MIDI Output OK")
except Exception as e:
    print(f"❌ MIDI Output HATA: {e}")
```

#### CV Output Test
```python
# CV çıkış testi
from sequencer.cv_output import cvOutput

try:
    cv = cvOutput(13, 26, 27, 21)
    cv.sendCv(0, 2048)  # Orta değer (~2.5V)
    cv.gateOn()
    time.sleep(0.5)
    cv.gateOff()
    print("✅ CV Output OK")
except Exception as e:
    print(f"❌ CV Output HATA: {e}")
```

### 2. Sistem Entegrasyon Testi

#### Tam Sistem Testi
```python
# Komple sistem testi
def full_system_test():
    """Tüm sistemi test et"""
    print("🔄 BABI SEQ Sistem Testi Başlatılıyor...")
    
    # 1. Hardware kontrolü
    print("1. Hardware testi...")
    test_hardware()
    
    # 2. Sequencer testi
    print("2. Sequencer testi...")
    test_sequencer()
    
    # 3. UI testi
    print("3. UI testi...")
    test_ui()
    
    # 4. Müzik modu testi
    print("4. Müzik modu testi...")
    test_music_modes()
    
    print("✅ Sistem testi tamamlandı!")

full_system_test()
```

## 🐛 Sorun Giderme

### Yaygın Problemler ve Çözümleri

#### 1. Pico Tanınmıyor
```bash
# Çözüm adımları:
1. USB kablosunu kontrol edin (data + power)
2. BOOTSEL tuşuna basarak yeniden bağlayın
3. Farklı USB portu deneyin
4. MicroPython firmware'i yeniden yükleyin
```

#### 2. TFT Ekran Çalışmıyor
```python
# Pin kontrolleri:
# 1. SPI bağlantılarını kontrol edin
# 2. Güç beslemesini ölçün (3.3V)
# 3. Pin numaralarını config.py'de doğrulayın

# Test kodu:
from machine import SPI, Pin
spi = SPI(0, baudrate=40000000, sck=Pin(6), mosi=Pin(7))
print("SPI testi:", spi)
```

#### 3. MIDI Çıkış Yok
```python
# Kontrol listesi:
# 1. UART bağlantısını kontrol edin
# 2. Optocoupler (6N138) devresini kontrol edin
# 3. MIDI kablo ve bağlantısını kontrol edin

# Test kodu:
from machine import UART
uart = UART(0, baudrate=31250, tx=0, rx=1)
uart.write(b'\x90\x60\x7F')  # Test Note On
```

#### 4. Bellek Hatası
```python
# Bellek optimizasyonu:
import gc
gc.collect()
print(f"Serbest bellek: {gc.mem_free()} bytes")

# Büyük dosyaları lazy loading ile yükleyin
# JSON modlarını ihtiyaç halinde okuyun
```

#### 5. LED'ler Yanmıyor
```python
# WS2812B test:
from machine import Pin
import neopixel

np = neopixel.NeoPixel(Pin(22), 16)
np[0] = (255, 0, 0)  # İlk LED kırmızı
np.write()
```

### Debug Modları

#### Verbose Logging
```python
# config.py'ye ekleyin:
DEBUG_MODE = True
VERBOSE_LOGGING = True

# Kodunuzda kullanın:
if DEBUG_MODE:
    print(f"Debug: {message}")
```

#### Performance Monitoring
```python
import time

def monitor_performance(func):
    """Performans monitör decorator"""
    def wrapper(*args, **kwargs):
        start = time.ticks_ms()
        result = func(*args, **kwargs)
        end = time.ticks_ms()
        print(f"{func.__name__}: {time.ticks_diff(end, start)}ms")
        return result
    return wrapper
```

## 📞 Destek

Kurulum sırasında sorun yaşarsanız:

### GitHub Issues
- Teknik problemler için issue açın
- Logları ve hata mesajlarını paylaşın
- Hardware setup fotoğraflarını ekleyin

### E-posta Desteği
- **Akademik**: [alparslan.ozturk@std.yildiz.edu.tr](mailto:alparslan.ozturk@std.yildiz.edu.tr)
- **Teknik**: GitHub Issues tercih edilir

### Faydalı Kaynaklar
- **MicroPython Dökümantasyonu**: [docs.micropython.org](https://docs.micropython.org)
- **Raspberry Pi Pico**: [raspberrypi.org/documentation](https://www.raspberrypi.org/documentation/)
- **ILI9341 Datasheet**: [ilitek.com](https://www.ilitek.com)

## ✅ Kurulum Başarılı!

Kurulum tamamlandıktan sonra:

1. **Sistem Testi**: Tüm bileşenleri test edin
2. **İlk Müzik**: Basit bir pattern oluşturun
3. **Konfigürasyon**: Kişisel ayarlarınızı yapın
4. **Backup**: Çalışan konfigürasyonu yedekleyin

**🎵 BABI SEQ ile müziğin mikrotonal dünyasını keşfetmeye başlayın! 🎵**
