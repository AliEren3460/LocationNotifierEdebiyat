#!/usr/bin/env python3
"""
Uygulama Test Scripti
Windows'ta uygulamayı test etmek için basit script
"""

import sys
import os

def test_imports():
    """Gerekli modülleri test et"""
    print("[TEST] Modul importlari test ediliyor...")
    
    try:
        import kivy
        print(f"[OK] Kivy {kivy.__version__}")
    except ImportError as e:
        print(f"[ERROR] Kivy import hatasi: {e}")
        return False
    
    try:
        import kivymd
        print(f"[OK] KivyMD")
    except ImportError as e:
        print(f"[ERROR] KivyMD import hatasi: {e}")
        return False
    
    try:
        import requests
        print(f"[OK] Requests")
    except ImportError as e:
        print(f"[ERROR] Requests import hatasi: {e}")
        return False
    
    try:
        import plyer
        print(f"[OK] Plyer")
    except ImportError as e:
        print(f"[ERROR] Plyer import hatasi: {e}")
        return False
    
    return True

def test_location_service():
    """Konum servisini test et"""
    print("\n[TEST] Konum servisi test ediliyor...")
    
    try:
        # Ana uygulamayı import et
        from main import LocationService
        
        service = LocationService()
        
        # Test konumu
        test_location = service._get_current_location()
        if test_location:
            print(f"[OK] Test konumu alindi: {test_location}")
            
            # Adres çözümleme testi
            address = service._reverse_geocode(test_location['lat'], test_location['lon'])
            print(f"[OK] Adres cozumleme: {address}")
            
            return True
        else:
            print("[WARNING] Konum alinamadi (normal - GPS yok)")
            return True
            
    except Exception as e:
        print(f"[ERROR] Konum servisi hatasi: {e}")
        return False

def test_ui():
    """UI'yi test et"""
    print("\n[TEST] UI test ediliyor...")
    
    try:
        from main import LocationTrackerApp
        
        print("[OK] Uygulama sinifi yuklendi")
        print("[INFO] UI testi icin 'python main.py' komutunu calistirin")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] UI test hatasi: {e}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("[TEST] Konum Takip Uygulamasi - Test Scripti")
    print("=" * 45)
    
    # Import testleri
    if not test_imports():
        print("\n[ERROR] Import testleri basarisiz!")
        print("[SOLUTION] python install_windows.py komutunu calistirin")
        return False
    
    # Konum servisi testi
    if not test_location_service():
        print("\n[ERROR] Konum servisi testi basarisiz!")
        return False
    
    # UI testi
    if not test_ui():
        print("\n[ERROR] UI testi basarisiz!")
        return False
    
    print("\n[SUCCESS] Tum testler basarili!")
    print("\n[NEXT STEPS]:")
    print("1. python main.py - Uygulamayi calistir")
    print("2. python build_apk.py - APK olustur")
    
    return True

if __name__ == '__main__':
    main()
