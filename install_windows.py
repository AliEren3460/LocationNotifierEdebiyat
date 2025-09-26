#!/usr/bin/env python3
"""
Windows Kurulum Scripti
Kivy ve diğer bağımlılıkları Windows'ta kurmak için
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Komutu çalıştır ve sonucu göster"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} başarılı!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} başarısız!")
        print(f"Hata: {e.stderr}")
        return False

def install_dependencies():
    """Bağımlılıkları yükle"""
    print("🚀 Windows için Kivy kurulumu başlatılıyor...")
    
    # Pip'i güncelle
    if not run_command("python -m pip install --upgrade pip", "Pip güncelleme"):
        return False
    
    # Kivy bağımlılıklarını Windows için yükle
    dependencies = [
        "wheel",
        "setuptools",
        "cython",
        "docutils",
        "pygments",
        "pypiwin32",
        "kivy_deps.sdl2",
        "kivy_deps.glew",
        "kivy_deps.gstreamer",
    ]
    
    print("\n📦 Kivy bağımlılıkları yükleniyor...")
    for dep in dependencies:
        if not run_command(f"python -m pip install {dep}", f"{dep} yükleme"):
            print(f"⚠️ {dep} yüklenemedi, devam ediliyor...")
    
    # Kivy'yi yükle
    if not run_command("python -m pip install kivy[base]==2.2.0", "Kivy yükleme"):
        # Alternatif yöntem
        print("🔄 Alternatif yöntemle Kivy yükleniyor...")
        if not run_command("python -m pip install kivy", "Kivy alternatif yükleme"):
            return False
    
    # Diğer paketleri yükle
    other_packages = [
        "kivymd==1.1.1",
        "requests==2.31.0",
        "plyer==2.1.0",
    ]
    
    for package in other_packages:
        run_command(f"python -m pip install {package}", f"{package} yükleme")
    
    return True

def test_installation():
    """Kurulumu test et"""
    print("\n🧪 Kurulum test ediliyor...")
    
    test_code = """
try:
    import kivy
    print(f"[OK] Kivy {kivy.__version__} basariyla yuklendi!")
    
    import kivymd
    print(f"[OK] KivyMD basariyla yuklendi!")
    
    import requests
    print(f"[OK] Requests basariyla yuklendi!")
    
    import plyer
    print(f"[OK] Plyer basariyla yuklendi!")
    
    print("\\n[SUCCESS] Tum paketler basariyla yuklendi!")
    
except ImportError as e:
    print(f"[ERROR] Import hatasi: {e}")
    exit(1)
"""
    
    try:
        result = subprocess.run([sys.executable, "-c", test_code], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Test başarısız: {e.stderr}")
        return False

def main():
    """Ana fonksiyon"""
    print("🖥️  Windows için Konum Takip Uygulaması Kurulumu")
    print("=" * 50)
    
    # Python versiyonunu kontrol et
    python_version = sys.version_info
    print(f"🐍 Python versiyonu: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 7):
        print("❌ Python 3.7 veya üzeri gerekli!")
        return False
    
    # Bağımlılıkları yükle
    if not install_dependencies():
        print("\n❌ Kurulum başarısız!")
        return False
    
    # Kurulumu test et
    if not test_installation():
        print("\n❌ Test başarısız!")
        return False
    
    print("\n🎉 Kurulum başarıyla tamamlandı!")
    print("\n📋 Sonraki adımlar:")
    print("1. python main.py - Uygulamayı test edin")
    print("2. python build_apk.py - APK oluşturun")
    
    return True

if __name__ == '__main__':
    main()
