# config.py - Düzeltilmiş versiyon
# Bu dosya, tüm yapılandırma değerlerini içeren merkezi bir konfigurasyon dosyasıdır
# Diğer tüm modüller tarafından bu dosyadan değerler alınır

# ----- Genel Ayarlar -----
# Ekran güncelleme aralığı (ms)
displayUpdateInterval = 200

# Buton sayısı (shift register'lar ile kontrol edilen)
buttonCount = 32  # Toplam buton sayısı

# Buton debounce süresi (ms)
buttonDebounceTime = 50  # ms

# ----- Donanım Pinleri -----
# UART/MIDI Pinleri
midiTxPin = 0          # UART0 TX pini
midiRxPin = 1          # UART0 RX pini

# TFT Ekran için SPI0 (Donanım SPI)
tftCs = 5              # TFT CS
tftSck = 6             # SPI0 SCK (Donanım SPI0)
tftMosi = 7            # SPI0 MOSI (Donanım SPI0)
tftDc = 3              # TFT DC
tftRst = 2             # TFT RESET
tftMiso = 4            # TFT Miso Backlight - 3.3V'a bağlı olduğu için bu pin kullanılmayacak

# TFT Dokunmatik Ekran Pinleri
touchCs = 8            # T_CS
touchClk = 9           # T_CLK
touchDin = 10          # T_DIN
touchDo = 11           # T_DO
touchIrq = 12          # T_IRQ

# DAC'ler İçin SPI1 (Donanım SPI)
dac1Cs = 13            # DAC #1 CS
dac2Cs = 14            # DAC #2 CS
dacSck = 26            # SPI1 SCK (Donanım SPI1)
dacMosi = 27           # SPI1 MOSI (Donanım SPI1)

# Encoder
encClk = 15            # Encoder CLK
encDt = 16             # Encoder DT
encSw = 17             # Encoder SW

# Shift Register
buttonDataPin = 18     # Button DATA
buttonClockPin = 19    # Button CLOCK
buttonLoadPin = 20     # Button LOAD

# LED Şerit (Opsiyonel)
ledStripPin = 22       # WS2812B veri pini
ledStripCount = 32     # Toplam LED sayısı

# ----- Sequencer Ayarları -----
# Sequencer varsayılan değerleri
defaultStepCount = 16  # Toplam adım sayısı
defaultMidiNote = 69   # A4 = 440Hz
defaultTempo = 120     # BPM
defaultGateTime = 0.5  # Nota süresi (oransal, 0.1-1.0 arası)

# Encoder debounce süresi
encoderDebounceTime = 5  # ms

# ----- Dosya Sistemi Ayarları -----
# Dahili flash'ta dosyaların kaydedileceği dizin
ModsDir = "mods"

# ----- Fontlar -----
mainFont = "fonts/Unispace12x24.c"
smallFont = "fonts/miniFont.h"  # Mini font 

# ----- TFT Ekran Boyutları -----
screenWidth = 240
screenHeight = 320

# ----- UI Renk Ayarları -----
# Renk değerleri (R, G, B) formatında 0-255 arası
# Renk değerleri None olmamalı! Tuple formatında tam sayıları içermeli
colorBackground = (0, 0, 0)        # Arka plan rengi
colorPrimary = (0, 0, 120)         # Ana renk
colorSecondary = (0, 100, 0)       # İkincil renk
colorAccent = (100, 0, 0)          # Vurgu rengi
colorText = (255, 255, 255)        # Metin rengi
colorTextSecondary = (200, 200, 200)  # İkincil metin rengi
colorSelected = (0, 255, 0)        # Seçili öğe rengi
colorPlaying = (255, 0, 0)         # Çalınan adım rengi
colorMuted = (50, 20, 0)           # Mute edilmiş adım rengi
colorSolo = (0, 50, 0)             # Solo adım rengi

# ----- Uygulama Sürümü -----
appVersion = "2.0.0"  # Yazılım sürümü
appName = "BABI SEQ"  # Uygulama adı