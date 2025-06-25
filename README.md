## 📚 Kullanılan Açık Kaynak Kütüphaneler

Bu proje aşağıdaki açık kaynak kütüphanelerini kullanmaktadır:

### Üçüncü Parti Kütüphaneler
| Kütüphane | Yazar | Lisans | Kullanım Amacı |
|-----------|-------|--------|----------------|
| [ili9341](https://github.com/rdagger/micropython-ili9341) | rdagger | MIT | TFT ekran sürücüsü (240x320) |
| [xpt2046](lib/xpt2046.py) | MicroPython Community | MIT | Dokunmatik ekran kontrolü |
| [xglcd_font](https://github.com/T-622/RdaggerXGLCD) | T-622 | MIT | Font rendering sistemi |
| [urequests2](https://github.com/chrisb2/micropython-lib) | Chris Borrill | MIT | HTTP istekleri (geliştirilmiş) |
| [touch_keyboard](https://github.com/rdagger/micropython-ili9341) | rdagger | MIT | Dokunmatik klavye |

### MicroPython Platform
| Modül | Versiyon | Kullanım Amacı |
|-------|----------|----------------|
| `machine` | 1.20+ | GPIO, SPI, UART, Timer |
| `neopixel` | 1.20+ | WS2812B LED kontrolü |
| `framebuf` | 1.20+ | Frame buffer operations |
| `json` | 1.20+ | JSON veri işleme |

### Font Dosyaları
| Dosya | Kaynak | Lisans | Format |
|-------|--------|--------|--------|
| `Unispace12x24.c` | MikroElektronika | Free Use | C bitmap |
| `miniFont.h` | M# BABI SEQ - Mikrotonal Dizi Destekli Sequencer

![BABI SEQ Logo](https://img.shields.io/badge/BABI_SEQ-v2.0.0-blue)
![Platform](https://img.shields.io/badge/Platform-Raspberry_Pi_Pico-green)
![Language](https://img.shields.io/badge/Language-MicroPython-yellow)
![License](https://img.shields.io/badge/License-MIT-red)
![Academic](https://img.shields.io/badge/Academic-Master's_Thesis-purple)

## 📖 Proje Hakkında

**BABI SEQ** *(Analog-Modüler Ses Sentezleyiciler İçin Mikrotonal Dizi Destekli Sequencer Tasarımı)*, Yıldız Teknik Üniversitesi Yüksek Lisans tezi kapsamında geliştirilen akademik araştırma projesidir.

### 🎓 Akademik Bağlam

Bu proje, **Yıldız Teknik Üniversitesi Sosyal Bilimler Enstitüsü Sanat ve Tasarım Ana Bilim Dalı Müzik ve Sahne Sanatları Yüksek Lisans Programı** kapsamında **Prof. Dr. Arda Eden** danışmanlığında gerçekleştirilmiştir.

**Araştırma Motivasyonu**: Müzik teknolojilerinin gelişimi, 20. yüzyıldan bu yana Batı müziğinin 12-ton eşit tamperaman paradigması çerçevesinde şekillenmiştir. Bu durum, Türk makam müziği ve diğer mikrotonal sistemlerin elektronik platformlarda özgün temsilinde belirgin eksiklikler yaratmaktadır.

**Araştırma Hedefi**: Analog-modüler sentezleyici ekosistemleri için mikrotonal dizi destekli sequencer sisteminin tasarım ve geliştirme sürecini kapsayarak, mevcut teknolojik çözümlerden farklı bakış açısı ortaya koymak ve metodolojik çeşitliliği zenginleştirmek.

### 🔬 Akademik Katkılar

- **Mikrotonal Müzik Teknolojileri**: 500+ dünya müzik modu içeren sistematik kütüphane
- **Hibrit Analog-Dijital Mimari**: Raspberry Pi Pico merkezli yenilikçi yaklaşım
- **Türk Makam Entegrasyonu**: İsmail Hakkı Özkan'ın kuramsal çerçevesi referans alınarak koma aralıklarının hesaplanması
- **Hassasiyet Standardları**: MIDI çıkışında ±1 cent hassasiyet, CV çıkışında ±5mV doğruluk
- **Tonal Tutarlılık**: Geleneksel icra ile elektronik üretim arasında kanıtlanmış uyumluluk

### ✨ Temel Özellikler

- **16 Adımlı Sekansör**: Tam programlanabilir step sequencer
- **Çift Çıkış**: MIDI ve CV/Gate çıkışları
- **Mikrotonal Destek**: 20+ farklı müzik kültüründen 500+ mod desteği
- **TFT Dokunmatik Ekran**: 240x320 piksel renkli ekran
- **Hardware Kontroller**: 28 buton + 1 encoder + 16 LED
- **Pattern Yönetimi**: JSON tabanlı mod kaydetme/yükleme
- **Rastgele Modlar**: Normal ve tam rastgele çalma modları

### 🎵 Desteklenen Müzik Modları

Proje, akademik araştırma kapsamında derlenen 500+ mod içerir:

#### Türk Müziği (200+ Makam)
- **Temel Makamlar**: Hicaz, Kürdi, Rast, Uşşak, Buselik
- **Şed Makamlar**: Nihavend, Hüseyni, Neva, Çargâh
- **Mürekkeb Makamlar**: Hicazkâr, Suzidil, Ferahfeza
- **Terkib Makamlar**: Şehnaz, Gerdaniye, Muhayyer

#### Dünya Müzik Kültürleri
- **Arap Müziği**: 45+ Maqam sistemi
- **Hint Müziği**: 70+ Raga sistemi  
- **Çin Müziği**: 25+ Pentatonik modlar
- **Afrika Müziği**: 20+ Geleneksel gamlar
- **Balkan Müziği**: Asimetrik modlar
- **Fars Müziği**: 35+ Geleneksel mod
- **Jazz**: 30+ Modern harmony
- **Mikrotonal**: Deneysel gamlar

## 📚 Kullanılan Açık Kaynak Kütüphaneler

Bu proje aşağıdaki açık kaynak kütüphanelerini kullanmaktadır:

### Üçüncü Parti Kütüphaneler
| Kütüphane | Yazar | Lisans | Kullanım Amacı |
|-----------|-------|--------|----------------|
| [ili9341](https://github.com/rdagger/micropython-ili9341) | rdagger | MIT | TFT ekran sürücüsü (240x320) |
| [xpt2046](lib/xpt2046.py) | MicroPython Community | MIT | Dokunmatik ekran kontrolü |
| [xglcd_font](https://github.com/T-622/RdaggerXGLCD) | T-622 | MIT | Font rendering sistemi |
| [urequests2](https://github.com/chrisb2/micropython-lib) | Chris Borrill | MIT | HTTP istekleri (geliştirilmiş) |
| [touch_keyboard](https://github.com/rdagger/micropython-ili9341) | rdagger | MIT | Dokunmatik klavye |

### MicroPython Platform
| Modül | Versiyon | Kullanım Amacı |
|-------|----------|----------------|
| `machine` | 1.20+ | GPIO, SPI, UART, Timer |
| `neopixel` | 1.20+ | WS2812B LED kontrolü |
| `framebuf` | 1.20+ | Frame buffer operations |
| `json` | 1.20+ | JSON veri işleme |

### Font Dosyaları
| Dosya | Kaynak | Lisans | Format |
|-------|--------|--------|--------|
| `Unispace12x24.c` | MikroElektronika | Free Use | C bitmap |
| `miniFont.h` | MikroElektronika | Free Use | C header |

**📄 Detaylı Lisans Bilgileri**: Tüm üçüncü parti kütüphanelerin detaylı lisans bilgileri, kaynak attributions ve akademik referanslar [THIRD_PARTY.md](THIRD_PARTY.md) dosyasında yer almaktadır.

**🎓 Akademik Atıf**: Tez çalışmasında kullanılan tüm kaynakların BibTeX formatındaki referansları [TEZ_KAYNAKCA.md](TEZ_KAYNAKCA.md) dosyasında bulunmaktadır.

---

## 🛠️ Donanım Gereksinimleri

### Ana Bileşenler
- **Raspberry Pi Pico** (RP2040)
- **ILI9341 TFT Ekran** (240x320, SPI)
- **XPT2046 Dokunmatik Kontroller**
- **MCP4822 DAC** (CV çıkışı için)
- **74HC165 Shift Register** (butonlar için)
- **Rotary Encoder** (parametre ayarları)
- **WS2812B LED Şerit** (16 LED)

### Pin Bağlantıları

#### MIDI/UART
```
GPIO 0  → MIDI TX
GPIO 1  → MIDI RX
```

#### TFT Ekran (SPI0)
```
GPIO 2  → TFT RESET
GPIO 3  → TFT DC
GPIO 4  → TFT MISO (Backlight)
GPIO 5  → TFT CS
GPIO 6  → TFT SCK
GPIO 7  → TFT MOSI
```

#### Dokunmatik Ekran
```
GPIO 8  → TOUCH CS
GPIO 9  → TOUCH CLK
GPIO 10 → TOUCH DIN
GPIO 11 → TOUCH DO
GPIO 12 → TOUCH IRQ
```

#### CV Çıkışı (SPI1)
```
GPIO 13 → CV CS (MCP4822)
GPIO 21 → CV GATE
GPIO 26 → CV SCK
GPIO 27 → CV MOSI
```

#### Kontroller
```
GPIO 15 → Encoder CLK
GPIO 16 → Encoder DT
GPIO 17 → Encoder SW
GPIO 18 → Button DATA (74HC165)
GPIO 19 → Button CLOCK
GPIO 20 → Button LOAD
GPIO 22 → LED Strip (WS2812B)
```

---

## 💻 Yazılım Kurulumu

### 1. MicroPython Kurulumu

Raspberry Pi Pico'ya MicroPython firmware yükleyin:

1. [MicroPython firmware dosyasını](https://micropython.org/download/rp2-pico/) indirin
2. Pico'yu BOOTSEL tuşuna basarak bilgisayara bağlayın
3. `.uf2` dosyasını RPI-RP2 sürücüsüne kopyalayın

### 2. Proje Dosyalarını Yükleme

```bash
# Proje klasörünü indirin
git clone https://github.com/kullanici-adi/babi-seq.git
cd babi-seq

# Tüm dosyaları Pico'ya yükleyin (Thonny IDE kullanarak)
```

#### Klasör Yapısı
```
babi-seq/
├── main.py                 # Ana uygulama
├── config.py              # Yapılandırma
├── features/               # Özellik modülleri
│   ├── playback.py        # Çalma kontrolü
│   ├── transpose.py       # Transpoze işlemleri
│   ├── random_modes.py    # Rastgele modlar
│   └── step_config.py     # Adım yapılandırması
├── hardware/               # Donanım sürücüleri
│   ├── buttons.py         # Buton yöneticisi
│   ├── encoders.py        # Encoder yöneticisi
│   ├── display.py         # Ekran yöneticisi
│   └── leds.py            # LED yöneticisi
├── sequencer/              # Sekansör motoru
│   ├── step_controller.py # Adım kontrolü
│   ├── midi_output.py     # MIDI çıkışı
│   ├── cv_output.py       # CV/Gate çıkışı
│   └── pattern_manager.py # Pattern yönetimi
├── ui/                     # Kullanıcı arayüzü
│   ├── menu_system.py     # Menü sistemi
│   ├── screen_manager.py  # Ekran yöneticisi
│   └── input_handler.py   # Girdi işleyici
├── lib/                    # Kütüphaneler
├── fonts/                  # Font dosyaları
└── mods/                   # Müzik modları (JSON)
    ├── Turkish_A-G.json   # Türk makamları
    ├── Arabic.json        # Arap makamları
    ├── Indian.json        # Hint ragaları
    └── ...
```

### 3. İlk Çalıştırma

```python
# main.py otomatik olarak çalışacaktır
# Veya REPL'de manuel başlatın:
import main
main.main()
```

---

## 🎛️ Kullanım Kılavuzu

### Buton Layout

```
[1 ] [2 ] [3 ] [4 ]     [17] [18] [19] [20]
[5 ] [6 ] [7 ] [8 ]     [21] [22] [23] [24]
[9 ] [10] [11] [12]     [25] [26] [27] [28]
[13] [14] [15] [16]     
```

#### Step Butonları (1-16)
- **Tek tık**: Adım seç/seçimi kaldır
- **Shift + Buton**: Çoklu seçim

#### Kontrol Butonları
- **17 - FREQ/NOTE**: Frekans/MIDI modu değiştir
- **18 - VELOCITY**: Velocity ayar modu
- **20 - PLAY/PAUSE**: Çalma kontrolü
- **21 - STOP**: Durdurma
- **22 - MUTE**: Seçili adımları sustur
- **23 - SOLO**: Seçili adımları solo yap
- **24 - SHIFT**: Shift tuşu
- **25 - TEMPO**: Tempo değiştir
- **26 - MENU**: Ana menü
- **27 - TRANSPOSE**: Transpoze modu
- **28 - RANDOM**: Rastgele çalma

### Encoder Kullanımı

- **Çevirme**: Seçili parametreyi değiştir
- **Basma**: Tüm adımları seç/seçimi kaldır

### Menü Sistemi

**Ana Menü** (Buton 26 ile erişin):
1. **Pattern İşlemleri**
   - Pattern Kaydet
   - Pattern Yükle  
   - Yeni Pattern
2. **Konfigürasyon**
   - Konfig. Kaydet
   - Konfig. Yükle
3. **MIDI Ayarları**

---

## 🎼 Mod Sistemi

### JSON Format Örneği

```json
{
  "name": "Hicaz",
  "fundamentalNote": "D",
  "fundamentalFrequency": 293.66,
  "totalSteps": 16,
  "steps": [
    {"step": 1, "frequency": 293.66, "note": "D", "cents": 0},
    {"step": 2, "frequency": 311.13, "note": "Eb", "cents": 100},
    {"step": 3, "frequency": 347.65, "note": "F#", "cents": 300},
    ...
  ]
}
```

### Desteklenen Müzik Kültürleri

| Dosya | İçerik | Mod Sayısı |
|-------|--------|------------|
| `Turkish_A-G.json` | Türk Makamları (A-G) | 80+ |
| `Arabic.json` | Arap Makamları | 45+ |
| `Indian.json` | Hint Ragaları | 70+ |
| `Persian.json` | Fars Makamları | 35+ |
| `Chinese.json` | Çin Modları | 25+ |
| `African.json` | Afrika Gamları | 20+ |
| `Jazz.json` | Jazz Modları | 30+ |

---

## ⚙️ Yapılandırma

### config.py Ayarları

```python
# MIDI Ayarları
defaultTempo = 120        # Varsayılan tempo (BPM)
defaultMidiNote = 69      # A4 = 440Hz
defaultGateTime = 0.5     # Gate süresi (0.1-1.0)

# Ekran Ayarları
screenWidth = 240
screenHeight = 320
displayUpdateInterval = 200  # ms

# Renk Ayarları
colorBackground = (0, 0, 0)
colorPrimary = (0, 0, 120)
colorSelected = (0, 255, 0)
colorPlaying = (255, 0, 0)
```

### Hardware Pin Ayarları

Tüm pin numaraları `config.py` dosyasında merkezi olarak tanımlanmıştır:

```python
# MIDI Pinleri
midiTxPin = 0
midiRxPin = 1

# TFT Pinleri  
tftCs = 5
tftSck = 6
tftMosi = 7
# ... diğer pinler
```

---

## 🔧 Geliştirici Bilgileri

### Sınıf Mimarisi

#### Ana Sınıflar
- **`StepController`**: Adım verilerini yönetir
- **`MidiOutput`**: MIDI mesajları ve zamanlama
- **`CVOutput`**: Analog CV/Gate çıkışı
- **`DisplayManager`**: TFT ekran kontrolü
- **`PatternManager`**: JSON mod yönetimi

#### Veri Akışı
```
Step → StepController → MidiOutput/CVOutput → Hardware
                    ↓
              DisplayManager → TFT Ekran
```

### Yeni Özellik Ekleme

#### 1. Yeni Buton İşlevi

`ui/input_handler.py` dosyasında:

```python
def _handleButtons(self, pressedButtons, shiftPressed):
    # Yeni buton (örnek: buton 29)
    if 29 in pressedButtons:
        self._yeniOzellik()

def _yeniOzellik(self):
    print("Yeni özellik çalıştırıldı")
    # Özellik kodunuz
```

#### 2. Yeni Mod Formatı

`mods/` klasörüne yeni JSON dosyası ekleyin:

```json
{
  "collections": [{
    "collectionName": "Yeni Müzik Kültürü",
    "modes": [
      {
        "name": "Yeni Mod",
        "steps": [...]
      }
    ]
  }]
}
```

### Debug Bilgileri

Debug mesajları için:

```python
# Bellek durumu kontrol
import gc
gc.collect()
print(f"Serbest bellek: {gc.mem_free()} bytes")

# MIDI mesaj takibi
# midi_output.py dosyasında debug modunu aktifleştirin
```

---

## 🐛 Sorun Giderme

### Yaygın Problemler

#### 1. Ekran Görünmüyor
```python
# config.py'de pin kontrolü
tftCs = 5    # Doğru pin?
tftSck = 6   # SPI0 bağlantısı kontrol edin
```

#### 2. MIDI Çıkış Yok
```python
# UART test
from machine import UART
uart = UART(0, baudrate=31250, tx=0, rx=1)
uart.write(b'\x90\x60\x7F')  # Test notu
```

#### 3. Butonlar Çalışmıyor
```python
# Shift register test
from hardware.buttons import ButtonManager
buttons = ButtonManager()
print(buttons.getPressedButtons())
```

#### 4. CV Çıkışı Yok
```python
# DAC test
from sequencer.cv_output import cvOutput
cv = cvOutput(13, 26, 27, 21)
cv.sendCv(0, 2048)  # Orta değer (~2.5V)
cv.gateOn()
```

### Bellek Yönetimi

```python
# Düzenli bellek temizliği
import gc
gc.collect()

# Büyük dosyaları yavaş yükleyin
# JSON modları lazy loading ile yükleyin
```

### Performans İpuçları

- **Timer Ayarları**: Ana döngü 10ms, ekran 200ms güncelleme
- **JSON Optimizasyonu**: Büyük mod dosyalarını parçalayın
- **LED Güncelleme**: Sadece değişen LED'leri güncelleyin

---

## 📚 API Referansı

### StepController

```python
# Adım seçimi
stepController.selectStep(stepNumber, clearOthers=True)

# Değer ayarlama
stepController.adjustValue(delta)

# Mute/Solo
stepController.muteStep(stepNumber)
stepController.soloStep(stepNumber)
```

### MidiOutput

```python
# Çalma kontrolü
midiOutput.start()
midiOutput.pause()
midiOutput.stop()

# Tempo ayarı
midiOutput.setTempo(120)  # BPM

# Transpoze
midiOutput.setTransposeAmount(semitones)
```

### PatternManager

```python
# Pattern kaydetme/yükleme
patternManager.savePattern("pattern_adi.json")
patternManager.loadPattern("pattern_adi.json")

# Pattern listesi
patterns = patternManager.listPatterns()
```

---

## 🤝 Katkı Sağlama

### Geliştirme Süreci

1. **Fork** edin
2. **Feature branch** oluşturun (`git checkout -b yeni-ozellik`)
3. **Commit** edin (`git commit -am 'Yeni özellik eklendi'`)
4. **Push** edin (`git push origin yeni-ozellik`)
5. **Pull Request** oluşturun

### Kod Standartları

- **PEP 8** Python kodlama standartları
- **Docstring** tüm fonksiyonlar için
- **Type Hints** mümkün olduğunca
- **Türkçe yorumlar** kod içinde

### Test Prosedürü

```python
# Donanım testleri
python tests/test_hardware.py

# Sequencer testleri  
python tests/test_sequencer.py

# UI testleri
python tests/test_ui.py
```

---

## 📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 👨‍🎓 Yazar & İletişim

**Alparslan Öztürk**  
*Yüksek Lisans Öğrencisi*  
Yıldız Teknik Üniversitesi  
Sosyal Bilimler Enstitüsü  
Sanat ve Tasarım Ana Bilim Dalı  
Müzik ve Sahne Sanatları Yüksek Lisans Programı  

**ORCID**: [0009-0003-8037-5071](https://orcid.org/0009-0003-8037-5071)

### 📧 İletişim
- **Akademik E-posta**: [alparslan.ozturk@std.yildiz.edu.tr](mailto:alparslan.ozturk@std.yildiz.edu.tr)
- **Kişisel Web**: [www.alparslanozturk.com.tr](https://www.alparslanozturk.com.tr)
- **GitHub**: [@alparslan-ozturk](https://github.com/alparslan-ozturk)

### 🌐 Sosyal Medya
- **Instagram**: [@aranjorofficial](https://instagram.com/aranjorofficial)
- **Facebook**: [@AranjorOfficial](https://facebook.com/AranjorOfficial)
- **X (Twitter)**: [@AranjorOfficial](https://x.com/AranjorOfficial)
- **LinkedIn**: [aranjoroficial](https://linkedin.com/in/aranjoroficial)

### 🎯 Danışman
**Prof. Dr. Arda Eden**  
Yıldız Teknik Üniversitesi  
Sanat ve Tasarım Fakültesi  

---

## 🙏 Teşekkürler

- **Prof. Dr. Arda Eden** - Tez danışmanı ve akademik rehberlik
- **Yıldız Teknik Üniversitesi** - Sosyal Bilimler Enstitüsü desteği
- **Sanat ve Tasarım Fakültesi** - Akademik altyapı desteği
- **MicroPython Topluluğu** - Platform desteği ve açık kaynak kütüphaneleri
- **Dünya Müzik Kültürleri** - Mikrotonal mod veritabanı kaynakları
- **İsmail Hakkı Özkan** - Türk Müziği Nazariyatı kuramsal çerçevesi

## 📚 Akademik Referanslar

- Özkan, İ. H. (2006). *Türk Mûsıkîsi Nazariyatı ve Usûlleri*. Ötüken Neşriyat.
- Yarman, O. (2008). *79-tone tuning & theory for Turkish maqam music*. 
- Arel, H. S. (1968). *Türk mûsıkîsi kimindir*.
- Signell, K. (1977). *Makam: Modal practice in Turkish art music*.

## 📄 Tez Bilgileri

**Başlık**: Analog-Modüler Ses Sentezleyiciler İçin Mikrotonal Dizi Destekli Sequencer Tasarımı: BABİ SEQ

**Enstitü**: Yıldız Teknik Üniversitesi Sosyal Bilimler Enstitüsü

**Program**: Sanat ve Tasarım Ana Bilim Dalı - Müzik ve Sahne Sanatları Yüksek Lisans Programı

**Yıl**: 2025

**Tez Türü**: Yüksek Lisans Tezi

**Danışman**: Prof. Dr. Arda Eden

### 📊 Özet
Müzik teknolojilerinin gelişimi, 20. yüzyıldan bu yana Batı müziğinin 12-ton eşit tamperaman paradigması çerçevesinde şekillenmiştir. Bu durum, Türk makam müziği ve diğer mikrotonal sistemlerin elektronik platformlarda özgün temsilinde belirgin eksiklikler yaratmaktadır. BABi SEQ projesi, analog-modüler sentezleyici ekosistemleri için mikrotonal dizi destekli sequencer sisteminin tasarım ve geliştirme sürecini kapsamaktadır.

**🎯 Araştırma Katkısı**: Mikrotonal müzik teknolojileri literatürüne alternatif metodolojik yaklaşım kazandırmak ve geleneksel müzik sistemlerinin çağdaş elektronik müzik üretiminde entegrasyonuna yönelik yeni perspektifler sunmak.

---

## 📈 Versiyon Geçmişi

### v2.0.0 (2025)
- ✅ 16 adımlı sequencer
- ✅ MIDI + CV çıkışı
- ✅ 500+ müzik modu
- ✅ TFT dokunmatik ekran
- ✅ Pattern yönetimi

### v1.0.0 (2024)
- ✅ Temel MIDI sequencer
- ✅ 8 adım desteği
- ✅ Basit LCD ekran

---

**🎵 BABI SEQ ile müziğin sınırlarını keşfedin! 🎵**
