# Katkı Sağlama Kılavuzu / Contributing Guide

BABI SEQ projesine katkı sağlamak istediğiniz için teşekkür ederiz! Bu kılavuz, projeye nasıl katkıda bulunabileceğinizi açıklar.

## 🎯 Katkı Türleri

### 1. Müzik Modları
- **Yeni Kültürel Modlar**: Eksik olan müzik kültürlerinden modlar
- **Mod Doğrulama**: Mevcut modların tonal doğruluğunu kontrol
- **Mikrotonal Sistemler**: Yeni deneysel gamlar

### 2. Kod Geliştirme
- **Bug Düzeltmeleri**: Hata raporları ve çözümleri
- **Yeni Özellikler**: Hardware/software özellikleri
- **Optimizasyon**: Performans iyileştirmeleri
- **Dokümantasyon**: Kod dokümantasyonu ve yorumlar

### 3. Hardware Desteği
- **Yeni Sensörler**: Ek hardware entegrasyonu
- **PCB Tasarımları**: Profesyonel board tasarımları
- **Case Tasarımları**: 3D printable kasalar

### 4. Dokümantasyon
- **Kullanım Kılavuzları**: Detaylı kullanım talimatları
- **Video Tutorials**: Görsel eğitim materyalleri
- **Çeviriler**: Çok dilli dokümantasyon

## 🚀 Başlangıç

### 1. Repository'yi Fork Edin
```bash
# GitHub'da fork edin
# Sonra local'e clone edin:
git clone https://github.com/kullanici-adi/babi-seq.git
cd babi-seq
```

### 2. Geliştirme Ortamını Kurun
```bash
# MicroPython geliştirme ortamı
# Thonny IDE veya VS Code + MicroPython eklentisi
```

### 3. Yeni Branch Oluşturun
```bash
git checkout -b feature/yeni-ozellik
# veya
git checkout -b fix/hata-duzeltmesi
# veya
git checkout -b docs/dokumantasyon-guncelleme
```

## 📝 Geliştirme Standartları

### Kod Standartları

#### Python/MicroPython
```python
# PEP 8 standardını takip edin
# Türkçe yorumlar kullanın
def yeniOzellik(parametre1, parametre2):
    """
    Fonksiyon açıklaması Türkçe yazılmalı
    
    Args:
        parametre1: İlk parametre açıklaması
        parametre2: İkinci parametre açıklaması
        
    Returns:
        bool: İşlem başarılıysa True, değilse False
    """
    # Yorumlar Türkçe
    if parametre1 > 0:
        print(f"Değer: {parametre1}")
        return True
    return False
```

#### Değişken İsimlendirme
```python
# Türkçe değişken isimleri tercih edilir
secilenAdimlar = set()
midiCikis = None
transpozMiktari = 0

# Class isimleri İngilizce (mevcut yapıyla uyumluluk için)
class StepController:
    pass
```

#### Dosya Organizasyonu
```
yeni-ozellik/
├── __init__.py          # Paket tanımlayıcı
├── ana_modul.py         # Ana modül
├── yardimci_modul.py    # Yardımcı fonksiyonlar
└── test_modul.py        # Test dosyaları
```

### Hardware Standartları

#### Pin Konfigürasyonu
```python
# config.py'ye yeni pinler eklerken:
# Açıklayıcı isimler kullanın
yeniSensorPin = 28       # YENİ SENSOR pini
yeniSensorCs = 29        # YENİ SENSOR CS pini

# Pin kullanım belgelendirmesi
"""
Pin Kullanım Tablosu:
GPIO 28: Yeni Sensor Data
GPIO 29: Yeni Sensor CS
"""
```

### Müzik Modu Standartları

#### JSON Format
```json
{
  "name": "Yeni Mod",
  "fundamentalNote": "C",
  "fundamentalFrequency": 261.63,
  "totalSteps": 16,
  "character": "açıklayıcı karakter",
  "steps": [
    {
      "step": 1,
      "frequency": 261.63,
      "note": "C",
      "function": "Temel ses",
      "cents": 0,
      "comment": "Açıklama"
    }
  ],
  "metadata": {
    "regionalOrigin": "Köken bilgisi",
    "traditionalUse": "Geleneksel kullanım",
    "instruments": ["Enstrüman listesi"]
  }
}
```

#### Frekans Doğruluğu
- **Hassasiyet**: ±1 cent tolerans
- **Referans**: A4 = 440Hz
- **Hesaplama**: Matematiksel formül belirtilmeli

## 🧪 Test Prosedürü

### Kod Testleri
```python
# Her yeni özellik için test yazın
def test_yeni_ozellik():
    """Yeni özellik testi"""
    # Test senaryolarını yazın
    assert yeniOzellik(1, 2) == True
    assert yeniOzellik(-1, 2) == False
    print("✅ Yeni özellik testleri geçti")
```

### Hardware Testleri
```python
# Hardware bileşenlerini test edin
def test_hardware():
    """Hardware test fonksiyonu"""
    # Pin bağlantılarını kontrol et
    # Sensor okumalarını doğrula
    # Çıkış sinyallerini ölç
    pass
```

### Müzik Modu Testleri
```python
# Mod dosyalarını doğrulayın
def test_muzik_modu():
    """Müzik modu doğrulama"""
    # JSON format kontrolü
    # Frekans hesaplama doğruluğu
    # Metadata eksiksizliği
    pass
```

## 📤 Pull Request Süreci

### 1. Commit Mesajları
```bash
# Türkçe commit mesajları kullanın
git commit -m "feat: Yeni CV çıkış desteği eklendi"
git commit -m "fix: MIDI timing hatası düzeltildi"
git commit -m "docs: Kullanım kılavuzu güncellendi"

# Commit tipleri:
# feat: Yeni özellik
# fix: Hata düzeltmesi
# docs: Dokümantasyon
# style: Kod formatı
# refactor: Kod yeniden düzenleme
# test: Test ekleme/düzeltme
# chore: Diğer değişiklikler
```

### 2. Pull Request Şablonu
```markdown
## Değişiklik Türü
- [ ] Bug düzeltmesi
- [ ] Yeni özellik
- [ ] Dokümantasyon güncelleme
- [ ] Müzik modu ekleme
- [ ] Hardware desteği

## Açıklama
Yaptığınız değişiklikleri detaylı açıklayın.

## Test Edildi
- [ ] Kod testleri geçti
- [ ] Hardware testi yapıldı
- [ ] Müzik modu doğrulandı

## Ekran Görüntüleri
Varsa ekran görüntüleri ekleyin.

## Checklist
- [ ] Kod PEP 8 standardına uygun
- [ ] Yorumlar Türkçe eklendi
- [ ] Test dosyaları eklendi
- [ ] Dokümantasyon güncellendi
```

### 3. Review Süreci
1. **Otomatik Kontroller**: Kod formatı ve temel testler
2. **Peer Review**: Diğer geliştiricilerden geri bildirim
3. **Hardware Test**: Fiziksel donanımda test
4. **Müzik Doğrulama**: Müzik modları için tonal doğruluk
5. **Merge**: Onaylandıktan sonra ana branch'e birleştirme

## 🐛 Bug Raporlama

### Issue Şablonu
```markdown
**Bug Açıklaması**
Hatayı kısaca açıklayın.

**Tekrar Üretme Adımları**
1. '...' yapın
2. '...' tıklayın
3. Hatayı görün

**Beklenen Davranış**
Ne olmasını beklediğinizi açıklayın.

**Ekran Görüntüleri**
Varsa ekran görüntüleri ekleyin.

**Ortam Bilgileri**
- Raspberry Pi Pico Firmware: [örn. v1.20.0]
- MicroPython Version: [örn. 1.20.0]
- Hardware: [örn. ILI9341 TFT]

**Ek Bilgiler**
Diğer önemli detaylar.
```

## 🎼 Müzik Modu Katkıları

### Yeni Kültür Ekleme
1. **Araştırma**: Akademik kaynakları kontrol edin
2. **Referans**: Güvenilir müzik teorisi kitapları
3. **Doğrulama**: Geleneksel müzisyenlerden onay
4. **Dokümantasyon**: Kaynak belgeleri ekleyin

### Mod Format Örneği
```json
{
  "project": "Babi SEQ Digital-Analog Sequencer",
  "institution": "YILDIZ TEKNIK UNIVERSITESI, Music Technologies",
  "author": "Katkıda Bulunan Kişi",
  "collections": [{
    "collectionName": "Yeni Müzik Kültürü",
    "culturalOrigin": "Coğrafi köken",
    "description": "Kültürel açıklama",
    "modes": [...]
  }]
}
```

## 🏆 Katkıda Bulunanlar

Katkıda bulunan herkesi `CONTRIBUTORS.md` dosyasında listeleyeceğiz:

### Kategoriler
- **Kod Geliştirme**: Ana kod katkıları
- **Müzik Modları**: Müzik teorisi katkıları
- **Hardware**: Donanım tasarımı
- **Dokümantasyon**: Belgelendirme
- **Test**: Kalite güvence
- **Çeviri**: Çok dilli destek

## 📞 İletişim

Sorularınız için:

- **GitHub Issues**: Teknik konular için
- **E-posta**: [alparslan.ozturk@std.yildiz.edu.tr](mailto:alparslan.ozturk@std.yildiz.edu.tr)
- **Web**: [www.alparslanozturk.com.tr](https://www.alparslanozturk.com.tr)

## 📄 Lisans

Katkılarınız MIT Lisansı kapsamında yayınlanacaktır. Katkıda bulunarak bu lisans şartlarını kabul etmiş sayılırsınız.

## 🎯 Özel Katkı Alanları

### Akademik Araştırma Desteği
- **Müzik Teorisi**: Mikrotonal sistemler araştırması
- **Akustik Analiz**: Frekans doğrulama çalışmaları
- **Kültürel Müzik**: Etnomüzikoloji katkıları
- **Teknoloji Entegrasyonu**: Yeni paradigma önerileri

### Eğitim Materyalleri
- **Workshop İçerikleri**: Pratik eğitim materyalleri
- **Video Tutorials**: Görsel öğretim içerikleri
- **Akademik Posterler**: Konferans sunumu materyalleri
- **Demonstrasyon Videoları**: Canlı performans örnekleri

## 🔗 Faydalı Bağlantılar

- **Proje Ana Sayfası**: [GitHub Repository](https://github.com/kullanici-adi/babi-seq)
- **Wiki**: Detaylı teknik dokümantasyon
- **Discussions**: Topluluk tartışmaları
- **Projects**: Geliştirme yol haritası

Katkılarınız için şimdiden teşekkür ederiz! 🎵
