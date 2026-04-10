import yt_dlp
import time

print("--- YOUTUBE GARANTİLİ İNDİRİCİ (VLC/FFmpeg Gerektirmez) ---")

link = input("Video linkini yapıştır: ")


ayarlar = {
    'format': '18',             
    'outtmpl': '%(title)s.%(ext)s', 
}

try:
    print("⏳ İndirme başladı... (Bu en güvenli yöntemdir)")
    
    with yt_dlp.YoutubeDL(ayarlar) as ydl:
        ydl.download([link])
        
    print("✅ İŞLEM BAŞARILI! Video klasörüne indi.")
    print("👉 İpucu: Önceki bozuk dosyayı silmeyi unutma!")

except Exception as hata:
    print("❌ HATA OLUŞTU!")
    print(hata)

time.sleep(5)