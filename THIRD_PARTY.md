# Üçüncü Parti Kütüphaneler / Third Party Libraries

Bu proje aşağıdaki açık kaynak kütüphanelerini kullanmaktadır. Her kütüphanenin orijinal lisansı ve telif hakkı bilgileri korunmuştur.

## 📚 Kullanılan Kütüphaneler

### 1. ILI9341 TFT Display Driver
- **Dosya**: `lib/ili9341.py`
- **Orijinal Kaynak**: [GitHub - rdagger/micropython-ili9341](https://github.com/rdagger/micropython-ili9341)
- **Yazar**: rdagger
- **Lisans**: MIT License
- **Açıklama**: ILI9341 TFT ekran sürücüsü (240x320 piksel)
- **Değişiklikler**: Rotation desteği ve Türkçe karakter adaptasyonu

```
MIT License - Copyright (c) 2019 rdagger
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

### 2. XPT2046 Touch Controller
- **Dosya**: `lib/xpt2046.py`
- **Orijinal Kaynak**: [GitHub - micropython community](https://github.com/micropython)
- **Yazar**: MicroPython Community Contributors
- **Lisans**: MIT License
- **Açıklama**: XPT2046 dokunmatik ekran kontrolcüsü
- **Değişiklikler**: BABI SEQ donanımı için kalibrasyon değerleri

### 3. XGLCD Font Library
- **Dosya**: `lib/xglcd_font.py`
- **Orijinal Kaynak**: [GitHub - T-622/RdaggerXGLCD](https://github.com/T-622/RdaggerXGLCD)
- **Yazar**: T-622, based on rdagger's work
- **Lisans**: MIT License
- **Açıklama**: X-GLCD formatında font rendering kütüphanesi
- **Değişiklikler**: MicroPython optimizasyonu ve bellek yönetimi

### 4. MicroPython urequests2
- **Dosya**: `lib/urequests2.py`
- **Orijinal Kaynak**: [GitHub - chrisb2/micropython-lib](https://github.com/chrisb2/micropython-lib/tree/master/urequests)
- **Yazar**: Chris Borrill (Chris2B)
- **Lisans**: MIT License
- **Açıklama**: Geliştirilmiş HTTP istekleri kütüphanesi (iter_lines desteği)
- **Değişiklikler**: Yok (orijinal haliyle kullanıldı)

```
MIT License - Forked from micropython/micropython-lib
Supports response.iter_lines() for memory-efficient REST API parsing
```

### 5. Touch Keyboard Library
- **Dosya**: `lib/touch_keyboard.py`
- **Orijinal Kaynak**: [GitHub - rdagger/micropython-ili9341](https://github.com/rdagger/micropython-ili9341)
- **Yazar**: rdagger
- **Lisans**: MIT License
- **Açıklama**: ILI9341 için dokunmatik klavye implementation
- **Değişiklikler**: BABI SEQ UI entegrasyonu için uyarlandı

### 6. Font Files
- **Dosyalar**: `fonts/Unispace12x24.c`, `fonts/miniFont.h`
- **Orijinal Kaynak**: MikroElektronika GLCD Font Creator
- **Yazar**: MikroElektronika
- **Lisans**: Free for personal and commercial use
- **Açıklama**: Bitmap font dosyaları (C formatında)
- **Değişiklikler**: MicroPython bytearray formatına dönüştürüldü

## 🛠️ MicroPython Platform Kütüphaneleri

### Yerleşik Modüller (Built-in)
Bu modüller MicroPython firmware'inin parçasıdır:

| Modül | Versiyon | Kullanım Amacı |
|-------|----------|----------------|
| `machine` | MicroPython 1.20+ | GPIO, SPI, UART, Timer kontrolü |
| `neopixel` | MicroPython 1.20+ | WS2812B RGB LED kontrolü |
| `framebuf` | MicroPython 1.20+ | Frame buffer operations |
| `time` | MicroPython 1.20+ | Zamanlama işlemleri |
| `json` | MicroPython 1.20+ | JSON veri işleme |
| `math` | MicroPython 1.20+ | Matematiksel hesaplamalar |
| `random` | MicroPython 1.20+ | Rastgele sayı üretimi |
| `gc` | MicroPython 1.20+ | Garbage collection (bellek yönetimi) |
| `os` | MicroPython 1.20+ | Dosya sistemi işlemleri |
| `sys` | MicroPython 1.20+ | Sistem bilgileri ve exception handling |

### Platform Lisansı
```
MicroPython License (MIT-based)
Copyright (c) 2013-2023 Damien P. George and contributors
Licensed under MIT License with additional terms for firmware distribution
```

## 🔧 Kütüphane Entegrasyonu ve Modifikasyonlar

### ILI9341 Adaptasyonları
```python
# ORİJİNAL KOD:
class Display:
    def __init__(self, spi, cs, dc, rst, width=320, height=240):

# BABI SEQ UYARLAMASI:
class Display:
    def __init__(self, spi, cs, dc, rst, width=320, height=240, rotation=90):
        # Rotation parametresi eklendi
        # BABI SEQ için optimize edilmiş çizim fonksiyonları
```

### XPT2046 Kalibrasyonu
```python
# BABI SEQ donanımına özel kalibrasyon değerleri:
self.x_min = 100
self.x_max = 1962  
self.y_min = 100
self.y_max = 1900
```

### Font Library Optimizasyonu
```python
# Bellek optimizasyonu için lazy loading:
def load_font_data(self, letter):
    # İhtiyaç anında font verisi yükleme
```

## ⚖️ Lisans Uyumluluğu

### MIT License Compliance
Tüm kullanılan MIT lisanslı kütüphaneler için:
- ✅ Orijinal copyright notice korundu
- ✅ License text preserved  
- ✅ Attribution provided
- ✅ Modifications documented
- ✅ Source links maintained

### Academic Use Compliance
Akademik çalışma için:
- ✅ Tüm kaynaklar documented
- ✅ Proper citations provided
- ✅ Fair use principles followed
- ✅ Open source ethics maintained

## 📖 Akademik Referanslar

### MicroPython Platform
```bibtex
@misc{micropython2023,
  title={MicroPython: Python for microcontrollers},
  author={George, Damien P. and Contributors},
  year={2023},
  url={https://micropython.org},
  note={Version 1.20+}
}
```

### ILI9341 Driver
```bibtex
@misc{rdagger2019ili9341,
  title={micropython-ili9341: ILI9341 TFT Display Driver for MicroPython},
  author={rdagger},
  year={2019},
  url={https://github.com/rdagger/micropython-ili9341},
  note={MIT License}
}
```

### XPT2046 Touch Controller
```bibtex
@misc{micropython2023xpt2046,
  title={XPT2046 Touch Screen Controller for MicroPython},
  author={MicroPython Community},
  year={2023},
  url={https://github.com/micropython/micropython-lib},
  note={MIT License}
}
```

### XGLCD Font Library
```bibtex
@misc{t622xglcd,
  title={RdaggerXGLCD: X-GLCD Font Library for MicroPython},
  author={T-622},
  url={https://github.com/T-622/RdaggerXGLCD},
  note={Based on rdagger's work, MIT License}
}
```

### Revised urequests
```bibtex
@misc{chrisb2urequests,
  title={Revised MicroPython urequests Library},
  author={Borrill, Chris},
  year={2020},
  url={https://github.com/chrisb2/micropython-lib/tree/master/urequests},
  note={Forked from micropython/micropython-lib, MIT License}
}
```

### MikroElektronika Fonts
```bibtex
@misc{mikroelektronika2011fonts,
  title={GLCD Font Creator},
  author={MikroElektronika},
  year={2011},
  url={http://www.mikroe.com/glcd-font-creator},
  note={Free for personal and commercial use}
}
```

## 🙏 Acknowledgments

Bu kütüphaneleri geliştiren tüm açık kaynak geliştiricilerine ve topluluklarına teşekkür ederiz:

- **Damien P. George** ve **MicroPython Community** - MicroPython platform
- **rdagger** - ILI9341 sürücüsü ve touch keyboard
- **Chris Borrill (Chris2B)** - Geliştirilmiş urequests kütüphanesi  
- **T-622** - XGLCD font library adaptasyonu
- **MikroElektronika** - Font creation tools
- **MicroPython Contributors** - Çeşitli hardware sürücüleri

## 📚 Ek Kaynaklar

### Donanım Datasheetleri
- [ILI9341 Datasheet](https://cdn-shop.adafruit.com/datasheets/ILI9341.pdf)
- [XPT2046 Datasheet](https://www.buydisplay.com/download/ic/XPT2046.pdf)
- [MCP4822 Datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/20002249B.pdf)
- [74HC165 Datasheet](https://www.ti.com/lit/ds/symlink/sn74hc165.pdf)

### Akademik Çalışmalar
- George, D. P. (2016). *MicroPython: a lean and efficient Python 3 implementation for microcontrollers and constrained systems*. Proceedings of the 45th International Conference on Parallel Processing Workshops.

## 📞 Lisans ve Attribution Soruları

Kütüphane kullanımı ve lisans uyumluluğu konusunda sorularınız için:
- **E-posta**: [alparslan.ozturk@std.yildiz.edu.tr](mailto:alparslan.ozturk@std.yildiz.edu.tr)
- **GitHub Issues**: Teknik sorular için issue açın
- **Academic**: Prof. Dr. Arda Eden (Tez Danışmanı)

---

*Bu dosya, açık kaynak etik ilkelerine ve akademik dürüstlük standartlarına uygun olarak hazırlanmıştır ve düzenli olarak güncellenmektedir.*
