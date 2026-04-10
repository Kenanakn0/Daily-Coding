import os

print("--- GÖREV YÖNETİCİSİ V3.0 (Tam Sürüm) ---")

dosya_adi = "gorevlerim.txt"
yapilacaklar = []

print("📂 Dosya kontrol ediliyor...")

if os.path.exists(dosya_adi):
    dosya = open(dosya_adi, "r", encoding="utf-8")
    for satir in dosya:
        temiz_veri = satir.strip()
        if len(temiz_veri) > 0: 
            yapilacaklar.append(temiz_veri)
    dosya.close()
    print(f"✅ {len(yapilacaklar)} adet eski görev yüklendi!")
else:
    print("ℹ️ Daha önce kayıtlı dosya yok, sıfırdan başlıyoruz.")


while True:
    print("\n" + "="*20)
    print(f"LİSTEDE {len(yapilacaklar)} GÖREV VAR")
    print("1. Ekle")
    print("2. Listele")
    print("3. Sil")
    print("4. KAYDET ve ÇIK")
    
    secim = input("Seçiminiz: ")

    if secim == '1':
        yeni_gorev = input("Yapılacak iş: ")
        yapilacaklar.append(yeni_gorev)
        print("➕ Eklendi.")

    elif secim == '2':
        print("\n--- GÖREVLERİNİZ ---")
        if len(yapilacaklar) == 0:
            print("Listeniz boş, keyfine bak! 😎")
        else:
            for numara, is_adi in enumerate(yapilacaklar, 1):
                print(f"{numara}. {is_adi}")

    elif secim == '3':
        print("\n--- SİLME EKRANI ---")
        for numara, is_adi in enumerate(yapilacaklar, 1):
            print(f"{numara}. {is_adi}")
        
        sil_no = int(input("Silinecek numarasını girin: "))
        try:
            silinen = yapilacaklar.pop(sil_no - 1)
            print(f"🗑️ '{silinen}' silindi.")
        except:
            print("❌ Hatalı numara girdiniz!")

    elif secim == '4':
        print("💾 Dosyaya kaydediliyor...")
        
        dosya = open(dosya_adi, "w", encoding="utf-8")
        for gorev in yapilacaklar:
            dosya.write(gorev + "\n")
        dosya.close()
        
        print("✅ Kayıt Başarılı! Dosyanız: " + dosya_adi)
        print("Güle güle! 👋")
        break