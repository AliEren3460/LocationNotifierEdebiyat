#!/usr/bin/env python3
"""
APK Build Script
Bu script Android APK dosyasını oluşturmak için buildozer kullanır
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Gerekli araçları kontrol et"""
    print("🔍 Gerekli araçlar kontrol ediliyor...")
    
    required_tools = {
        'python': 'Python 3.7+',
        'java': 'Java JDK 8+',
        'git': 'Git',
    }
    
    missing_tools = []
    
    for tool, description in required_tools.items():
        try:
            result = subprocess.run([tool, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ {tool}: {description}")
            else:
                missing_tools.append((tool, description))
        except (subprocess.TimeoutExpired, FileNotFoundError):
            missing_tools.append((tool, description))
    
    if missing_tools:
        print("\n❌ Eksik araçlar:")
        for tool, description in missing_tools:
            print(f"   - {tool}: {description}")
        return False
    
    return True

def install_buildozer():
    """Buildozer'ı yükle"""
    print("\n📦 Buildozer yükleniyor...")
    
    try:
        # Buildozer'ı pip ile yükle
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'buildozer'], 
                      check=True)
        print("✅ Buildozer başarıyla yüklendi")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Buildozer yüklenemedi: {e}")
        return False

def setup_android_environment():
    """Android geliştirme ortamını ayarla"""
    print("\n🔧 Android ortamı ayarlanıyor...")
    
    # Android SDK ve NDK otomatik olarak indirilecek
    print("📱 Android SDK ve NDK buildozer tarafından otomatik indirilecek")
    
    return True

def build_apk():
    """APK dosyasını oluştur"""
    print("\n🏗️  APK oluşturuluyor...")
    
    try:
        # Debug APK oluştur
        print("🔨 Debug APK oluşturuluyor...")
        result = subprocess.run(['buildozer', 'android', 'debug'], 
                               capture_output=True, text=True, timeout=1800)
        
        if result.returncode == 0:
            print("✅ Debug APK başarıyla oluşturuldu!")
            
            # APK dosyasının konumunu bul
            bin_dir = Path('./bin')
            if bin_dir.exists():
                apk_files = list(bin_dir.glob('*.apk'))
                if apk_files:
                    apk_file = apk_files[0]
                    print(f"📱 APK dosyası: {apk_file.absolute()}")
                    
                    # APK dosyasını ana dizine kopyala
                    shutil.copy2(apk_file, './konum_takip.apk')
                    print("📁 APK dosyası ana dizine kopyalandı: konum_takip.apk")
            
            return True
        else:
            print(f"❌ APK oluşturulamadı:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Build işlemi zaman aşımına uğradı (30 dakika)")
        return False
    except Exception as e:
        print(f"❌ Build hatası: {e}")
        return False

def build_release_apk():
    """Release APK oluştur"""
    print("\n🚀 Release APK oluşturuluyor...")
    
    try:
        result = subprocess.run(['buildozer', 'android', 'release'], 
                               capture_output=True, text=True, timeout=1800)
        
        if result.returncode == 0:
            print("✅ Release APK başarıyla oluşturuldu!")
            
            # Release APK dosyasını bul
            bin_dir = Path('./bin')
            if bin_dir.exists():
                apk_files = list(bin_dir.glob('*-release-unsigned.apk'))
                if apk_files:
                    apk_file = apk_files[0]
                    print(f"📱 Release APK: {apk_file.absolute()}")
                    
                    # Release APK'yı ana dizine kopyala
                    shutil.copy2(apk_file, './konum_takip_release.apk')
                    print("📁 Release APK ana dizine kopyalandı: konum_takip_release.apk")
            
            return True
        else:
            print(f"❌ Release APK oluşturulamadı:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Release build hatası: {e}")
        return False

def main():
    """Ana fonksiyon"""
    print("🚀 Konum Takip Uygulaması - APK Build Script")
    print("=" * 50)
    
    # Gerekli araçları kontrol et
    if not check_requirements():
        print("\n❌ Lütfen eksik araçları yükleyin ve tekrar deneyin.")
        return False
    
    # Buildozer'ı yükle
    if not install_buildozer():
        return False
    
    # Android ortamını ayarla
    if not setup_android_environment():
        return False
    
    # Kullanıcıya seçenek sun
    print("\n📋 Build seçenekleri:")
    print("1. Debug APK (test için)")
    print("2. Release APK (yayın için)")
    print("3. Her ikisi")
    
    choice = input("\nSeçiminizi yapın (1-3): ").strip()
    
    success = True
    
    if choice in ['1', '3']:
        success &= build_apk()
    
    if choice in ['2', '3']:
        success &= build_release_apk()
    
    if success:
        print("\n🎉 Build işlemi başarıyla tamamlandı!")
        print("\n📱 APK dosyalarını Android cihazınıza yükleyebilirsiniz.")
        print("⚠️  Bilinmeyen kaynaklardan uygulama yüklemeyi etkinleştirmeyi unutmayın.")
    else:
        print("\n❌ Build işlemi başarısız oldu.")
    
    return success

if __name__ == '__main__':
    main()
