#!/usr/bin/env python3
"""
Windows için APK Build Script
Buildozer ile Android APK oluşturma
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import time

def check_buildozer():
    """Buildozer kurulumunu kontrol et"""
    try:
        result = subprocess.run(['buildozer', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"[OK] Buildozer kurulu")
            return True
        else:
            print("[ERROR] Buildozer bulunamadi")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("[ERROR] Buildozer bulunamadi")
        return False

def initialize_buildozer():
    """Buildozer'ı başlat"""
    print("\n[INIT] Buildozer baslatiliyor...")
    
    try:
        # Buildozer init (eğer gerekirse)
        if not os.path.exists('buildozer.spec'):
            print("[INFO] buildozer.spec olusturuluyor...")
            result = subprocess.run(['buildozer', 'init'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                print(f"[ERROR] Buildozer init hatasi: {result.stderr}")
                return False
        
        print("[OK] Buildozer hazir")
        return True
        
    except Exception as e:
        print(f"[ERROR] Buildozer init hatasi: {e}")
        return False

def clean_buildozer():
    """Buildozer cache'ini temizle"""
    print("\n[CLEAN] Cache temizleniyor...")
    
    try:
        result = subprocess.run(['buildozer', 'android', 'clean'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("[OK] Cache temizlendi")
        else:
            print("[WARNING] Cache temizlenemedi, devam ediliyor...")
        
        return True
        
    except Exception as e:
        print(f"[WARNING] Cache temizleme hatasi: {e}")
        return True

def build_debug_apk():
    """Debug APK oluştur"""
    print("\n[BUILD] Debug APK olusturuluyor...")
    print("[INFO] Bu islem 10-30 dakika surebilir (ilk seferinde)...")
    
    try:
        # Buildozer debug komutunu çalıştır
        process = subprocess.Popen(
            ['buildozer', 'android', 'debug'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Çıktıyı gerçek zamanlı göster
        output_lines = []
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                output_lines.append(output)
        
        # Sonucu kontrol et
        if process.returncode == 0:
            print("\n[SUCCESS] Debug APK basariyla olusturuldu!")
            
            # APK dosyasını bul
            bin_dir = Path('./bin')
            if bin_dir.exists():
                apk_files = list(bin_dir.glob('*.apk'))
                if apk_files:
                    apk_file = apk_files[0]
                    print(f"[INFO] APK dosyasi: {apk_file.absolute()}")
                    
                    # APK'yı ana dizine kopyala
                    target_name = 'konum_takip_debug.apk'
                    shutil.copy2(apk_file, target_name)
                    print(f"[INFO] APK kopyalandi: {target_name}")
                    
                    return True
            
            print("[WARNING] APK dosyasi bulunamadi")
            return False
        else:
            print(f"\n[ERROR] Build basarisiz (exit code: {process.returncode})")
            
            # Hata analizi
            error_output = ''.join(output_lines)
            if 'JAVA_HOME' in error_output:
                print("[HINT] Java JDK kurulu degil veya JAVA_HOME ayarlanmamis")
            elif 'SDK' in error_output:
                print("[HINT] Android SDK indirme sorunu olabilir")
            elif 'NDK' in error_output:
                print("[HINT] Android NDK indirme sorunu olabilir")
            elif 'internet' in error_output.lower():
                print("[HINT] Internet baglantisi kontrol edin")
            
            return False
            
    except KeyboardInterrupt:
        print("\n[INFO] Build islemi kullanici tarafindan durduruldu")
        return False
    except Exception as e:
        print(f"\n[ERROR] Build hatasi: {e}")
        return False

def check_apk_output():
    """APK çıktısını kontrol et"""
    print("\n[CHECK] APK dosyalari kontrol ediliyor...")
    
    # Ana dizindeki APK dosyalarını bul
    apk_files = list(Path('.').glob('*.apk'))
    
    if apk_files:
        print("[SUCCESS] APK dosyalari bulundu:")
        for apk in apk_files:
            size = apk.stat().st_size / (1024 * 1024)  # MB
            print(f"  - {apk.name} ({size:.1f} MB)")
        
        print("\n[NEXT] APK dosyasini Android cihaziniza yukleyin:")
        print("1. APK dosyasini telefona kopyalayin")
        print("2. Bilinmeyen kaynaklara izin verin")
        print("3. APK'ya dokunarak yukleyin")
        print("4. Tum izinleri verin (konum, bildirim, arka plan)")
        
        return True
    else:
        print("[ERROR] APK dosyasi bulunamadi")
        return False

def main():
    """Ana fonksiyon"""
    print("[BUILD] Windows APK Build Script")
    print("=" * 40)
    
    # Buildozer kontrolü
    if not check_buildozer():
        print("\n[ERROR] Buildozer bulunamadi!")
        print("[SOLUTION] pip install buildozer komutunu calistirin")
        return False
    
    # Buildozer başlatma
    if not initialize_buildozer():
        return False
    
    # Kullanıcı onayı
    print("\n[INFO] APK build islemi baslatilacak")
    print("[WARNING] Bu islem uzun surebilir ve internet gerektirir")
    
    response = input("\nDevam etmek istiyor musunuz? (y/n): ").lower().strip()
    if response not in ['y', 'yes', 'evet', 'e']:
        print("[INFO] Build islemi iptal edildi")
        return False
    
    # Cache temizleme (opsiyonel)
    clean_response = input("\nCache temizlensin mi? (y/n): ").lower().strip()
    if clean_response in ['y', 'yes', 'evet', 'e']:
        clean_buildozer()
    
    # Debug APK oluştur
    if build_debug_apk():
        check_apk_output()
        print("\n[SUCCESS] Build islemi tamamlandi!")
        return True
    else:
        print("\n[ERROR] Build islemi basarisiz!")
        print("\n[TROUBLESHOOTING]:")
        print("1. Internet baglantinizi kontrol edin")
        print("2. Java JDK yuklu oldugunu kontrol edin")
        print("3. Disk alaninin yeterli oldugunu kontrol edin (5GB+)")
        print("4. buildozer android clean komutunu deneyin")
        return False

if __name__ == '__main__':
    main()
