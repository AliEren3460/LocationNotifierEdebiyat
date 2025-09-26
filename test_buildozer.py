#!/usr/bin/env python3
"""
Buildozer Test Script
Buildozer kurulumunu ve konfigürasyonunu test eder
"""

import subprocess
import os
import sys

def test_buildozer_installation():
    """Buildozer kurulumunu test et"""
    print("[TEST] Buildozer kurulumu test ediliyor...")
    
    try:
        result = subprocess.run(['buildozer', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"[OK] Buildozer kurulu: {result.stdout.strip()}")
            return True
        else:
            print(f"[ERROR] Buildozer hatasi: {result.stderr}")
            return False
    except FileNotFoundError:
        print("[ERROR] Buildozer bulunamadi")
        return False
    except Exception as e:
        print(f"[ERROR] Buildozer test hatasi: {e}")
        return False

def test_buildozer_config():
    """Buildozer konfigürasyonunu test et"""
    print("\n[TEST] Buildozer konfigurasyonu test ediliyor...")
    
    if not os.path.exists('buildozer.spec'):
        print("[ERROR] buildozer.spec dosyasi bulunamadi")
        return False
    
    try:
        result = subprocess.run(['buildozer', 'android', 'debug', '--dry-run'], 
                              capture_output=True, text=True, timeout=30)
        
        output = result.stdout + result.stderr
        
        if 'Check configuration tokens' in output:
            print("[OK] Buildozer konfigurasyonu gecerli")
            return True
        else:
            print("[ERROR] Buildozer konfigurasyonu hatali")
            print(f"Cikti: {output}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Konfigurasyon test hatasi: {e}")
        return False

def test_java():
    """Java kurulumunu test et"""
    print("\n[TEST] Java kurulumu test ediliyor...")
    
    try:
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            java_version = result.stderr.split('\n')[0]  # Java version stderr'da
            print(f"[OK] Java kurulu: {java_version}")
            return True
        else:
            print("[ERROR] Java bulunamadi")
            return False
    except Exception as e:
        print(f"[ERROR] Java test hatasi: {e}")
        return False

def test_git():
    """Git kurulumunu test et"""
    print("\n[TEST] Git kurulumu test ediliyor...")
    
    try:
        result = subprocess.run(['git', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"[OK] Git kurulu: {result.stdout.strip()}")
            return True
        else:
            print("[ERROR] Git bulunamadi")
            return False
    except Exception as e:
        print(f"[ERROR] Git test hatasi: {e}")
        return False

def show_build_requirements():
    """Build gereksinimleri göster"""
    print("\n[INFO] APK build gereksinimleri:")
    print("1. Python 3.7+ - [OK]")
    print("2. Java JDK 8+ - Test ediliyor...")
    print("3. Git - Test ediliyor...")
    print("4. Buildozer - Test ediliyor...")
    print("5. Internet baglantisi - Gerekli")
    print("6. Disk alani - En az 5GB")

def main():
    """Ana test fonksiyonu"""
    print("[TEST] Buildozer Build Hazirlik Testi")
    print("=" * 40)
    
    show_build_requirements()
    
    all_tests_passed = True
    
    # Java testi
    if not test_java():
        all_tests_passed = False
        print("[SOLUTION] Java JDK 8+ yukleyin: https://adoptium.net/")
    
    # Git testi
    if not test_git():
        all_tests_passed = False
        print("[SOLUTION] Git yukleyin: https://git-scm.com/")
    
    # Buildozer testi
    if not test_buildozer_installation():
        all_tests_passed = False
        print("[SOLUTION] pip install buildozer komutunu calistirin")
    else:
        # Konfigürasyon testi
        if not test_buildozer_config():
            all_tests_passed = False
    
    print("\n" + "=" * 40)
    
    if all_tests_passed:
        print("[SUCCESS] Tum testler basarili!")
        print("[INFO] APK build icin hazirsiniz")
        print("[NEXT] python build_windows.py komutunu calistirin")
    else:
        print("[ERROR] Bazi testler basarisiz!")
        print("[INFO] Yukaridaki cozumleri uygulayip tekrar deneyin")
    
    return all_tests_passed

if __name__ == '__main__':
    main()
