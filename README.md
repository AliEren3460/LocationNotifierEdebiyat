# 📱 Konum Takip Uygulaması

Python/Kivy ile geliştirilmiş, Android ve iOS'ta çalışabilen konum takip uygulaması. Uygulama arka planda çalışır ve her 2 dakikada bir konumunuzu il/ilçe bilgisiyle bildirim olarak gönderir.

## ✨ Özellikler

- 🌍 **GPS Konum Takibi**: Yüksek doğrulukta konum belirleme
- 🔄 **Arka Plan Çalışma**: Uygulama kapatıldığında bile çalışmaya devam eder
- 📍 **Adres Çözümleme**: Koordinatları il/ilçe bilgisine çevirir
- 🔔 **Düzenli Bildirimler**: Her 2 dakikada bir konum bildirimi
- 📱 **Çapraz Platform**: Android ve iOS desteği
- 🔋 **Pil Optimizasyonu**: Verimli arka plan çalışma

## 🛠️ Teknolojiler

- **Python 3.7+**
- **Kivy 2.1.0** - Mobil UI framework
- **KivyMD 1.1.1** - Material Design bileşenleri
- **Buildozer** - Android APK oluşturma
- **Plyer** - Platform-specific API erişimi
- **PyJNIus** - Android Java API erişimi

## 📋 Gereksinimler

### Geliştirme Ortamı
- Python 3.7 veya üzeri
- Java JDK 8 veya üzeri
- Git
- Android SDK (buildozer tarafından otomatik indirilir)
- Android NDK (buildozer tarafından otomatik indirilir)

### Python Paketleri
```bash
pip install -r requirements.txt
```

## 🚀 Kurulum ve Çalıştırma

### 1. Projeyi İndirin
```bash
git clone <repository-url>
cd location_tracker_app
```

### 2. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Desktop'ta Test Edin
```bash
python main.py
```

### 4. Android APK Oluşturun
```bash
python build_apk.py
```

## 📱 APK Oluşturma Süreci

### Otomatik Build (Önerilen)
```bash
python build_apk.py
```

Bu script:
- Gerekli araçları kontrol eder
- Buildozer'ı yükler
- Android ortamını ayarlar
- APK dosyasını oluşturur

### Manuel Build
```bash
# Buildozer'ı yükle
pip install buildozer

# İlk kez çalıştırma (Android SDK/NDK indirir)
buildozer android debug

# APK dosyası ./bin/ klasöründe oluşur
```

### Release APK (Play Store için)
```bash
buildozer android release
```

## 🔧 Konfigürasyon

### buildozer.spec Dosyası
- Uygulama adı, paket adı, versiyonu
- Android API seviyeleri
- İzinler ve gereksinimler
- Build ayarları

### Android İzinleri
- `ACCESS_FINE_LOCATION` - Hassas konum erişimi
- `ACCESS_COARSE_LOCATION` - Genel konum erişimi
- `ACCESS_BACKGROUND_LOCATION` - Arka plan konum erişimi
- `FOREGROUND_SERVICE` - Arka plan servisi
- `WAKE_LOCK` - Cihazı uyanık tutma
- `INTERNET` - İnternet erişimi
- `POST_NOTIFICATIONS` - Bildirim gönderme

## 📲 Kurulum (Android)

1. **APK Dosyasını İndirin**
   - `konum_takip.apk` (debug) veya
   - `konum_takip_release.apk` (release)

2. **Bilinmeyen Kaynaklara İzin Verin**
   - Ayarlar > Güvenlik > Bilinmeyen Kaynaklar ✅

3. **APK'yı Yükleyin**
   - Dosya yöneticisinden APK'ya dokunun
   - Yükleme izni verin

4. **İzinleri Verin**
   - Konum erişimi ✅
   - Bildirim izni ✅
   - Arka plan çalışma izni ✅

## 🎯 Kullanım

1. **Uygulamayı Açın**
2. **"Takibi Başlat" Butonuna Basın**
3. **İzinleri Onaylayın**
   - Konum erişimi
   - Bildirim izni
   - Arka plan çalışma
4. **Uygulamayı Kapatabilirsiniz**
   - Arka planda çalışmaya devam eder
5. **Her 2 Dakikada Bildirim Alırsınız**

## 🔔 Bildirim Formatı

```
📍 Konum Güncellendi
Şu anki konumunuz: Kadıköy / İstanbul
Güncelleme: 14:30
```

## 🐛 Sorun Giderme

### Konum Alınamıyor
- GPS'in açık olduğundan emin olun
- Konum izinlerini kontrol edin
- İnternet bağlantınızı kontrol edin

### Bildirim Gelmiyor
- Bildirim izinlerini kontrol edin
- Pil optimizasyonunu kapatın
- Arka plan çalışma izni verin

### APK Oluşturulamıyor
- Java JDK yüklü olduğundan emin olun
- İnternet bağlantınızı kontrol edin
- Disk alanınızı kontrol edin (en az 5GB)

### Build Hataları
```bash
# Buildozer cache'ini temizle
buildozer android clean

# Tekrar dene
buildozer android debug
```

## 🔒 Gizlilik

- Konum verileri sadece adres çözümleme için kullanılır
- Hiçbir veri sunucuda saklanmaz
- Sadece OpenStreetMap Nominatim API'si kullanılır
- Kişisel veriler üçüncü taraflarla paylaşılmaz

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📞 Destek

Sorularınız için:
- Issue oluşturun
- E-posta gönderin
- Dokümantasyonu inceleyin

## 🔄 Güncellemeler

### v1.0.0
- İlk sürüm
- Temel konum takibi
- Android desteği
- Bildirim sistemi

---

**⚠️ Önemli Notlar:**
- Uygulamayı sürekli çalıştırmak pil tüketimini artırabilir
- Konum verilerinin doğruluğu GPS sinyaline bağlıdır
- İlk kurulumda tüm izinleri verdiğinizden emin olun
