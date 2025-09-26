"""
Arka Plan Konum Servisi
Android'de arka planda çalışacak servis
"""

import time
import requests
from datetime import datetime
from kivy.logger import Logger
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass, cast
    from android import mActivity
    
    # Android sınıfları
    Context = autoclass('android.content.Context')
    NotificationManager = autoclass('android.app.NotificationManager')
    NotificationCompat = autoclass('androidx.core.app.NotificationCompat')
    NotificationChannel = autoclass('android.app.NotificationChannel')
    PendingIntent = autoclass('android.app.PendingIntent')
    Intent = autoclass('android.content.Intent')
    LocationManager = autoclass('android.location.LocationManager')
    Service = autoclass('android.app.Service')


class LocationBackgroundService:
    """Arka plan konum servisi"""
    
    def __init__(self):
        self.is_running = False
        self.notification_id = 1
        self.channel_id = "location_channel"
        
        if platform == 'android':
            self.setup_notification_channel()
    
    def setup_notification_channel(self):
        """Bildirim kanalını ayarla (Android 8.0+)"""
        if platform == 'android':
            try:
                context = mActivity
                notification_manager = context.getSystemService(Context.NOTIFICATION_SERVICE)
                
                # Bildirim kanalı oluştur
                channel = NotificationChannel(
                    self.channel_id,
                    "Konum Takip Bildirimleri",
                    NotificationManager.IMPORTANCE_DEFAULT
                )
                channel.setDescription("Konum güncellemeleri için bildirimler")
                notification_manager.createNotificationChannel(channel)
                
                Logger.info("Service: Bildirim kanalı oluşturuldu")
                
            except Exception as e:
                Logger.error(f"Service: Bildirim kanalı hatası - {str(e)}")
    
    def start_service(self):
        """Servisi başlat"""
        self.is_running = True
        Logger.info("Service: Arka plan servisi başlatıldı")
        
        # Foreground service olarak başlat
        if platform == 'android':
            self.start_foreground_service()
        
        # Ana döngü
        self.run_service_loop()
    
    def start_foreground_service(self):
        """Foreground service başlat"""
        if platform == 'android':
            try:
                context = mActivity
                
                # Foreground notification oluştur
                builder = NotificationCompat.Builder(context, self.channel_id)
                builder.setContentTitle("Konum Takip Aktif")
                builder.setContentText("Uygulama arka planda konum takibi yapıyor")
                builder.setSmallIcon(android.R.drawable.ic_dialog_info)
                builder.setPriority(NotificationCompat.PRIORITY_LOW)
                builder.setOngoing(True)  # Sürekli bildirim
                
                notification = builder.build()
                
                # Service'i foreground modda başlat
                service = autoclass('org.kivy.android.PythonService')
                service.startForeground(self.notification_id, notification)
                
                Logger.info("Service: Foreground service başlatıldı")
                
            except Exception as e:
                Logger.error(f"Service: Foreground service hatası - {str(e)}")
    
    def run_service_loop(self):
        """Ana servis döngüsü"""
        while self.is_running:
            try:
                # Konum al
                location = self.get_current_location()
                
                if location:
                    # Adres bilgisini al
                    address = self.reverse_geocode(location['lat'], location['lon'])
                    
                    # Bildirim gönder
                    self.send_location_notification(address)
                    
                    Logger.info(f"Service: Konum güncellendi - {address}")
                else:
                    Logger.warning("Service: Konum alınamadı")
                
                # 2 dakika bekle (120 saniye)
                time.sleep(120)
                
            except Exception as e:
                Logger.error(f"Service: Döngü hatası - {str(e)}")
                time.sleep(30)  # Hata durumunda 30 saniye bekle
    
    def get_current_location(self):
        """Mevcut konumu al"""
        if platform == 'android':
            try:
                context = mActivity
                location_manager = context.getSystemService(Context.LOCATION_SERVICE)
                
                # GPS ve Network provider'larını kontrol et
                providers = ['gps', 'network', 'passive']
                
                for provider in providers:
                    if location_manager.isProviderEnabled(provider):
                        last_location = location_manager.getLastKnownLocation(provider)
                        
                        if last_location:
                            return {
                                'lat': last_location.getLatitude(),
                                'lon': last_location.getLongitude(),
                                'provider': provider
                            }
                
                Logger.warning("Service: Hiçbir provider'dan konum alınamadı")
                return None
                
            except Exception as e:
                Logger.error(f"Service: GPS hatası - {str(e)}")
                return None
        else:
            # Test için sabit konum
            return {'lat': 41.0082, 'lon': 28.9784, 'provider': 'test'}
    
    def reverse_geocode(self, lat, lon):
        """Koordinatları adres bilgisine çevir"""
        try:
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json',
                'addressdetails': 1,
                'accept-language': 'tr',
                'zoom': 10
            }
            
            headers = {
                'User-Agent': 'LocationTracker/1.0'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                address = data.get('address', {})
                
                # Türkiye için il/ilçe bilgisi
                state = address.get('state', '')
                city = address.get('city', '') or address.get('town', '') or address.get('county', '')
                district = address.get('suburb', '') or address.get('neighbourhood', '')
                
                location_parts = []
                if district:
                    location_parts.append(district)
                if city and city != district:
                    location_parts.append(city)
                if state and state not in location_parts:
                    location_parts.append(state)
                
                if location_parts:
                    return " / ".join(location_parts)
                else:
                    return "Konum belirlenemedi"
            else:
                Logger.warning(f"Service: Geocoding API hatası - {response.status_code}")
                return "Adres bilgisi alınamadı"
                
        except requests.exceptions.Timeout:
            Logger.error("Service: Geocoding timeout")
            return "Bağlantı zaman aşımı"
        except Exception as e:
            Logger.error(f"Service: Reverse geocoding hatası - {str(e)}")
            return "Adres bilgisi hatası"
    
    def send_location_notification(self, location_text):
        """Konum bildirimi gönder"""
        if platform == 'android':
            try:
                context = mActivity
                notification_manager = context.getSystemService(Context.NOTIFICATION_SERVICE)
                
                # Bildirim oluştur
                builder = NotificationCompat.Builder(context, self.channel_id)
                builder.setContentTitle("📍 Konum Güncellendi")
                builder.setContentText(f"Şu anki konumunuz: {location_text}")
                builder.setSmallIcon(android.R.drawable.ic_dialog_info)
                builder.setPriority(NotificationCompat.PRIORITY_DEFAULT)
                builder.setAutoCancel(True)
                builder.setVibrate([0, 250, 250, 250])  # Titreşim
                
                # Zaman damgası ekle
                current_time = datetime.now().strftime("%H:%M")
                builder.setSubText(f"Güncelleme: {current_time}")
                
                notification = builder.build()
                notification_manager.notify(self.notification_id + 1, notification)
                
                Logger.info(f"Service: Bildirim gönderildi - {location_text}")
                
            except Exception as e:
                Logger.error(f"Service: Bildirim hatası - {str(e)}")
        else:
            # Desktop test için
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"🔔 [{current_time}] Konum Bildirimi: {location_text}")
    
    def stop_service(self):
        """Servisi durdur"""
        self.is_running = False
        Logger.info("Service: Arka plan servisi durduruldu")


def main():
    """Servis ana fonksiyonu"""
    Logger.info("Service: Arka plan servisi başlatılıyor...")
    
    service = LocationBackgroundService()
    service.start_service()


if __name__ == '__main__':
    main()
