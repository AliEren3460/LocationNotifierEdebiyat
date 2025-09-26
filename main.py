"""
Konum Takip Uygulaması
Android ve iOS için Python/Kivy ile geliştirilmiş
Arka planda çalışan konum takip ve bildirim sistemi
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.utils import platform

# Android için gerekli importlar
if platform == 'android':
    try:
        from android.permissions import request_permissions, Permission
        from android.broadcast import BroadcastReceiver
        from jnius import autoclass, cast
        from android import mActivity
        
        # Android sınıfları
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationCompat = autoclass('androidx.core.app.NotificationCompat')
        PendingIntent = autoclass('android.app.PendingIntent')
        Intent = autoclass('android.content.Intent')
    except ImportError:
        Logger.warning("Android modülleri yüklenemedi - Desktop modunda çalışılıyor")

import requests
import json
from datetime import datetime
import threading
import time

class LocationService:
    """Konum servisi sınıfı"""
    
    def __init__(self):
        self.is_running = False
        self.location_thread = None
        self.current_location = None
        
    def start_location_tracking(self):
        """Konum takibini başlat"""
        if platform == 'android':
            # Android izinlerini iste
            request_permissions([
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION,
                Permission.ACCESS_BACKGROUND_LOCATION,
                Permission.WAKE_LOCK,
                Permission.FOREGROUND_SERVICE
            ])
        
        self.is_running = True
        self.location_thread = threading.Thread(target=self._location_loop)
        self.location_thread.daemon = True
        self.location_thread.start()
        Logger.info("LocationService: Konum takibi başlatıldı")
    
    def stop_location_tracking(self):
        """Konum takibini durdur"""
        self.is_running = False
        if self.location_thread:
            self.location_thread.join()
        Logger.info("LocationService: Konum takibi durduruldu")
    
    def _location_loop(self):
        """Ana konum takip döngüsü"""
        while self.is_running:
            try:
                location = self._get_current_location()
                if location:
                    address = self._reverse_geocode(location['lat'], location['lon'])
                    self._send_notification(address)
                    Logger.info(f"LocationService: Konum güncellendi - {address}")
                
                # 2 dakika bekle
                time.sleep(120)
                
            except Exception as e:
                Logger.error(f"LocationService: Hata - {str(e)}")
                time.sleep(30)  # Hata durumunda 30 saniye bekle
    
    def _get_current_location(self):
        """Mevcut konumu al"""
        if platform == 'android':
            try:
                # Android GPS servisi
                LocationManager = autoclass('android.location.LocationManager')
                context = mActivity
                location_manager = context.getSystemService(Context.LOCATION_SERVICE)
                
                # En son bilinen konumu al
                providers = location_manager.getProviders(True)
                location = None
                
                for provider in providers.toArray():
                    last_location = location_manager.getLastKnownLocation(provider)
                    if last_location:
                        location = {
                            'lat': last_location.getLatitude(),
                            'lon': last_location.getLongitude()
                        }
                        break
                
                return location
                
            except Exception as e:
                Logger.error(f"GPS Hatası: {str(e)}")
                return None
        else:
            # Test için sabit konum (İstanbul)
            return {'lat': 41.0082, 'lon': 28.9784}
    
    def _reverse_geocode(self, lat, lon):
        """Koordinatları adres bilgisine çevir"""
        try:
            # Nominatim API kullanarak reverse geocoding
            url = f"https://nominatim.openstreetmap.org/reverse"
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json',
                'addressdetails': 1,
                'accept-language': 'tr'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                address = data.get('address', {})
                
                # Türkiye için il/ilçe bilgisi
                state = address.get('state', '')
                city = address.get('city', '') or address.get('town', '') or address.get('village', '')
                
                if state and city:
                    return f"{city}, {state}"
                elif state:
                    return state
                else:
                    return "Konum belirlenemedi"
            
        except Exception as e:
            Logger.error(f"Reverse geocoding hatası: {str(e)}")
        
        return "Adres bilgisi alınamadı"
    
    def _send_notification(self, location_text):
        """Bildirim gönder"""
        if platform == 'android':
            try:
                # Android bildirimi
                context = mActivity
                notification_manager = context.getSystemService(Context.NOTIFICATION_SERVICE)
                
                # Bildirim oluştur
                builder = NotificationCompat.Builder(context, "location_channel")
                builder.setContentTitle("Konum Güncellendi")
                builder.setContentText(f"Şu anki konumunuz: {location_text}")
                builder.setSmallIcon(android.R.drawable.ic_dialog_info)
                builder.setPriority(NotificationCompat.PRIORITY_DEFAULT)
                builder.setAutoCancel(True)
                
                notification = builder.build()
                notification_manager.notify(1, notification)
                
            except Exception as e:
                Logger.error(f"Bildirim hatası: {str(e)}")
        else:
            # Desktop için konsol çıktısı
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] Konum Bildirimi: {location_text}")


class LocationTrackerApp(App):
    """Ana uygulama sınıfı"""
    
    def __init__(self):
        super().__init__()
        self.location_service = LocationService()
        self.is_tracking = False
    
    def build(self):
        """UI oluştur"""
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Başlık
        title = Label(
            text='Konum Takip Uygulaması',
            size_hint_y=0.2,
            font_size='24sp'
        )
        layout.add_widget(title)
        
        # Durum etiketi
        self.status_label = Label(
            text='Konum takibi kapalı',
            size_hint_y=0.3,
            font_size='18sp'
        )
        layout.add_widget(self.status_label)
        
        # Başlat/Durdur butonu
        self.toggle_button = Button(
            text='Takibi Başlat',
            size_hint_y=0.2,
            font_size='20sp'
        )
        self.toggle_button.bind(on_press=self.toggle_tracking)
        layout.add_widget(self.toggle_button)
        
        # Bilgi etiketi
        info_label = Label(
            text='Uygulama arka planda çalışacak ve\nher 2 dakikada bir konum bildirim gönderecek.',
            size_hint_y=0.3,
            font_size='14sp',
            text_size=(None, None)
        )
        layout.add_widget(info_label)
        
        return layout
    
    def toggle_tracking(self, instance):
        """Takibi başlat/durdur"""
        if not self.is_tracking:
            self.start_tracking()
        else:
            self.stop_tracking()
    
    def start_tracking(self):
        """Takibi başlat"""
        self.location_service.start_location_tracking()
        self.is_tracking = True
        self.toggle_button.text = 'Takibi Durdur'
        self.status_label.text = 'Konum takibi aktif - Arka planda çalışıyor'
        
        # Android'de arka plan servisi başlat
        if platform == 'android':
            self.start_background_service()
    
    def stop_tracking(self):
        """Takibi durdur"""
        self.location_service.stop_location_tracking()
        self.is_tracking = False
        self.toggle_button.text = 'Takibi Başlat'
        self.status_label.text = 'Konum takibi kapalı'
    
    def start_background_service(self):
        """Android arka plan servisi başlat"""
        if platform == 'android':
            try:
                service = autoclass('org.kivy.android.PythonService')
                service.start(mActivity, '')
                Logger.info("Arka plan servisi başlatıldı")
            except Exception as e:
                Logger.error(f"Arka plan servisi hatası: {str(e)}")
    
    def on_pause(self):
        """Uygulama duraklatıldığında"""
        # Arka planda çalışmaya devam et
        return True
    
    def on_resume(self):
        """Uygulama devam ettirildiğinde"""
        pass


if __name__ == '__main__':
    LocationTrackerApp().run()
