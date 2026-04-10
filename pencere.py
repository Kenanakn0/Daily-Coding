import tkinter as tk
from tkinter import messagebox 
import yt_dlp

def indirme_baslat():
    link = link_kutusu.get() 
    
    if not link: 
        durum_yazisi.config(text="Lütfen bir link yapıştırın!", fg="red")
        return

    durum_yazisi.config(text="⏳ İndiriliyor... Lütfen bekleyin (Pencere donabilir)", fg="blue")
    pencere.update() 

    ayarlar = {
        'format': '22/18',
        'outtmpl': '%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ayarlar) as ydl:
            ydl.download([link])
        
        durum_yazisi.config(text="✅ İŞLEM BAŞARILI! Video indi.", fg="green")
        messagebox.showinfo("Başarılı", "Video başarıyla indirildi! 📂")
        
    except Exception as hata:
        durum_yazisi.config(text="❌ Hata oluştu!", fg="red")
        messagebox.showerror("Hata", f"Bir sorun çıktı:\n{hata}")

pencere = tk.Tk()
pencere.title("Süper YouTube İndirici v3.0")
pencere.geometry("500x250")


tk.Label(pencere, text="YouTube Video İndirici", font=("Arial", 16, "bold")).pack(pady=10)


tk.Label(pencere, text="Link:").pack()
link_kutusu = tk.Entry(pencere, width=50)
link_kutusu.pack(pady=5)


btn = tk.Button(pencere, text="VİDEOYU İNDİR ⬇️", bg="red", fg="white", font=("Arial", 11, "bold"), command=indirme_baslat)
btn.pack(pady=15)


durum_yazisi = tk.Label(pencere, text="Hazır", fg="grey")
durum_yazisi.pack(pady=10)

pencere.mainloop()
