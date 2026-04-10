import tkinter as tk
from tkinter import messagebox
import os


def dosya_yukle():
    if os.path.exists("gorevler.txt"):
        with open("gorevler.txt", "r", encoding="utf-8") as dosya:
            for satir in dosya:
                liste_kutusu.insert(tk.END, satir.strip())

def dosya_guncelle():
    
    tum_gorevler = liste_kutusu.get(0, tk.END) 
    with open("gorevler.txt", "w", encoding="utf-8") as dosya:
        for gorev in tum_gorevler:
            dosya.write(gorev + "\n")

def ekle():
    yeni_gorev = giris_kutusu.get()
    
    if yeni_gorev != "":
        liste_kutusu.insert(tk.END, yeni_gorev) 
        giris_kutusu.delete(0, tk.END) 
        dosya_guncelle()
    else:
        messagebox.showwarning("Uyarı", "Lütfen boş görev ekleme!")

def sil():
    try:
        secili_indeks = liste_kutusu.curselection()[0]
        liste_kutusu.delete(secili_indeks) 
        dosya_guncelle() 
    except:
        messagebox.showwarning("Hata", "Silmek için listeden bir görev seçmelisin!")

def sil():
    try:
        secili_indeks = liste_kutusu.curselection()[0]
        liste_kutusu.delete(secili_indeks)
        dosya_guncelle()

    except:
        messagebox.showwarning("Hata", "Silmek için listeden bir görev seçmelisin!")

pencere = tk.Tk()
pencere.title("Akıllı Ajanda v2.0")
pencere.geometry("400x500")
pencere.configure(bg="#e0f7fa")

tk.Label(pencere, text="YAPILACAKLAR LİSTESİ", bg="#e0f7fa", font=("Arial", 16, "bold")).pack(pady=15)
giris_kutusu = tk.Entry(pencere,width=30,font=("Arial",12))
giris_kutusu.pack(pady=5)

btn_ekle = tk.Button(pencere, text="GÖREV EKLE ➕", bg="green", fg="white", font=("Arial", 10, "bold"), command=ekle)
btn_ekle.pack(pady=5)

liste_kutusu = tk.Listbox(pencere, width=40, height=15, font=("Arial", 11), selectmode=tk.SINGLE)
liste_kutusu.pack(pady=10)

btn_sil = tk.Button(pencere, text="SEÇİLİ OLANI SİL 🗑️", bg="red", fg="white", font=("Arial", 10, "bold"), command=sil)
btn_sil.pack(pady=10)

dosya_yukle()
pencere.mainloop()