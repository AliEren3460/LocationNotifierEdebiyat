#!/usr/bin/env python3
"""
Hızlı Test - Sadece import kontrolü
"""

print("[TEST] Hizli import testi...")

try:
    import kivy
    print(f"[OK] Kivy {kivy.__version__} yuklendi")
except ImportError as e:
    print(f"[ERROR] Kivy yuklenemedi: {e}")
    exit(1)

try:
    import kivymd
    print("[OK] KivyMD yuklendi")
except ImportError as e:
    print(f"[ERROR] KivyMD yuklenemedi: {e}")
    exit(1)

try:
    import requests
    print("[OK] Requests yuklendi")
except ImportError as e:
    print(f"[ERROR] Requests yuklenemedi: {e}")
    exit(1)

try:
    import plyer
    print("[OK] Plyer yuklendi")
except ImportError as e:
    print(f"[ERROR] Plyer yuklenemedi: {e}")
    exit(1)

print("\n[SUCCESS] Tum paketler basariyla yuklendi!")
print("[INFO] Simdi 'python main.py' komutunu calistirabilisiniz")
