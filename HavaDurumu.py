import tkinter as tk
from tkinter import messagebox
import requests

api_key = "899b841756daa67cb115af27d808bacc" 

def hava_durumunu_getir():
    sehir = giris_kutusu.get() 
    
    if not sehir:
        messagebox.showwarning("Uyarı", "Lütfen bir şehir ismi gir!")
        return

    sonuc_etiketi.config(text="📡 Bağlanılıyor...", fg="blue")
    pencere.update()

    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&lang=tr&units=metric"

    try:
        cevap = requests.get(url)
        
        if cevap.status_code == 200:
            veri = cevap.json()
            
            sicaklik = veri['main']['temp']
            durum = veri['weather'][0]['description']
            hissedilen = veri['main']['feels_like']
            
            sonuc_etiketi.config(text=f"{sehir.upper()}\n{sicaklik}°C", fg="black", font=("Arial", 30, "bold"))
            detay_etiketi.config(text=f"{durum.upper()}\n(Hissedilen: {hissedilen}°C)", fg="gray")
            
        else:
            sonuc_etiketi.config(text="Bulunamadı!", fg="red")
            detay_etiketi.config(text="Şehir ismini kontrol et.")
            
    except Exception as hata:
        messagebox.showerror("Hata", f"Bir sorun oluştu:\n{hata}")

pencere = tk.Tk()
pencere.title("Hava Durumu Ajanı 🌤️")
pencere.geometry("300x400")
pencere.configure(bg="#f0f8ff") 


baslik = tk.Label(pencere, text="Hava Durumu", bg="#f0f8ff", font=("Arial", 16))
baslik.pack(pady=20)

giris_kutusu = tk.Entry(pencere, font=("Arial", 14), justify="center")
giris_kutusu.pack(pady=5)
giris_kutusu.insert(0, "Istanbul")

buton = tk.Button(pencere, text="SORGULA 🔍", bg="orange", fg="white", font=("Arial", 12, "bold"), command=hava_durumunu_getir)
buton.pack(pady=15)

sonuc_etiketi = tk.Label(pencere, text="--°C", bg="#f0f8ff", font=("Arial", 30, "bold"))
sonuc_etiketi.pack(pady=20)

detay_etiketi = tk.Label(pencere, text="Durum Bekleniyor...", bg="#f0f8ff", font=("Arial", 10))
detay_etiketi.pack()

pencere.mainloop()

print("Bu da yeni eklenen satir")

print("şimdi beni görmen lazım git")