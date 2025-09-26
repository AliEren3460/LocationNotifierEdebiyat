# 🖥️ Windows'ta APK Oluşturma Kılavuzu

## ⚠️ Önemli Not
Buildozer Windows'ta doğrudan çalışmaz. Aşağıdaki alternatif yöntemlerden birini kullanmanız gerekir.

## 🔧 Yöntem 1: WSL (Windows Subsystem for Linux) - ÖNERİLEN

### Adım 1: WSL Yükleyin
```powershell
# PowerShell'i yönetici olarak açın
wsl --install
# Bilgisayarı yeniden başlatın
```

### Adım 2: Ubuntu'da Buildozer Kurun
```bash
# WSL Ubuntu'yu açın
wsl

# Sistem güncellemesi
sudo apt update && sudo apt upgrade -y

# Gerekli paketleri yükleyin
sudo apt install -y python3-pip python3-venv git openjdk-8-jdk unzip

# Buildozer'ı yükleyin
pip3 install buildozer

# Android geliştirme araçları
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
```

### Adım 3: Proje Dosyalarını WSL'e Kopyalayın
```bash
# Windows dosyalarına erişim
cd /mnt/c/Users/aeren/CascadeProjects/location_tracker_app

# Veya WSL home'a kopyalayın
cp -r /mnt/c/Users/aeren/CascadeProjects/location_tracker_app ~/
cd ~/location_tracker_app
```

### Adım 4: APK Oluşturun
```bash
# İlk kez çalıştırma (SDK/NDK indirir)
buildozer android debug

# APK dosyası ./bin/ klasöründe oluşur
ls -la bin/
```

## 🔧 Yöntem 2: Docker Kullanımı

### Docker Desktop Yükleyin
1. Docker Desktop'u indirin: https://www.docker.com/products/docker-desktop
2. Yükleyin ve başlatın

### Buildozer Docker Container'ı Kullanın
```powershell
# Proje dizininde
cd C:\Users\aeren\CascadeProjects\location_tracker_app

# Docker ile buildozer çalıştırın
docker run --rm -v ${PWD}:/home/user/hostcwd kivy/buildozer android debug
```

## 🔧 Yöntem 3: GitHub Actions (Bulut Build)

### GitHub Repository Oluşturun
1. GitHub'da yeni repository oluşturun
2. Proje dosyalarını yükleyin

### GitHub Actions Workflow Oluşturun
`.github/workflows/build.yml` dosyası:

```yaml
name: Build APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer

    - name: Build APK
      run: |
        buildozer android debug

    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: apk
        path: bin/*.apk
```

## 🔧 Yöntem 4: Online Build Servisleri

### 1. Replit
- https://replit.com/ adresine gidin
- Python projesi oluşturun
- Dosyalarınızı yükleyin
- Terminal'de buildozer komutlarını çalıştırın

### 2. Google Colab
- https://colab.research.google.com/ adresine gidin
- Yeni notebook oluşturun
- Buildozer'ı yükleyin ve çalıştırın

## 📱 APK Test Etme

### Desktop'ta Test
```powershell
# Uygulamayı desktop'ta test edin
python main.py
```

### Android Emulator
1. Android Studio yükleyin
2. AVD Manager ile emulator oluşturun
3. APK'yı emulator'e yükleyin

## 🚀 Önerilen Yöntem: WSL

En kolay ve güvenilir yöntem WSL kullanmaktır:

1. **WSL yükleyin** (tek seferlik)
2. **Ubuntu'da buildozer kurun** (tek seferlik)
3. **Proje dosyalarını kopyalayın**
4. **APK oluşturun**

### WSL Kurulum Komutu
```powershell
# PowerShell (Yönetici)
wsl --install
```

### Buildozer Kurulum (WSL Ubuntu'da)
```bash
sudo apt update
sudo apt install -y python3-pip git openjdk-8-jdk
pip3 install buildozer
```

### APK Build (WSL Ubuntu'da)
```bash
cd ~/location_tracker_app
buildozer android debug
```

## 🎯 Sonuç

Windows'ta doğrudan buildozer çalışmadığı için WSL kullanmanız önerilir. Bu yöntem:
- ✅ En güvenilir
- ✅ En hızlı
- ✅ En kolay
- ✅ Microsoft tarafından desteklenen

APK oluşturduktan sonra Windows'tan Android cihazınıza yükleyebilirsiniz.

## 🆘 Yardım

Herhangi bir sorun yaşarsanız:
1. WSL kurulum kılavuzunu takip edin
2. Ubuntu terminal'de komutları çalıştırın
3. Hata mesajlarını paylaşın

Başarılar! 🚀
