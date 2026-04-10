class Islem: 
    def __init__(self, miktar, kategori, islem_tipi, aciklama=""):
        self.miktar = miktar
        self.kategori = kategori     # 
        self.islem_tipi = islem_tipi 
        self.aciklama = aciklama     

class FinansYoneticisi:
    def __init__(self):
        self.islemler = []
        
    def islem_ekle(self, miktar, kategori, islem_tipi, aciklama=""):
        yeni_islem = Islem(miktar, kategori, islem_tipi, aciklama)
        self.islemler.append(yeni_islem)
        print(f"İşlem Tamam: {miktar} TL cinsinden {islem_tipi} eklendi. ({kategori})")
        
    
    def bakiye_hesapla(self):
        bakiye = 0
        for islem in self.islemler:
            if islem.islem_tipi == "Gelir":
                bakiye += islem.miktar
            elif islem.islem_tipi == "Gider":
                bakiye -= islem.miktar
        return bakiye
        
    def ozet_goster(self):
        print("\nFinans Özetin")
        print("="*20)
        print(f"Güncel Bakiye: {self.bakiye_hesapla()} TL")
        print(f"Toplam İşlem Sayısı: {len(self.islemler)}")
        print("="*20 + "\n")


if __name__ == "__main__":
    cuzdan = FinansYoneticisi()

    cuzdan.islem_ekle(24000, "Maaş", "Gelir", "Haziran maaşı")
    cuzdan.islem_ekle(8000, "Kira", "Gider", "Haziran ayı kirası")
    cuzdan.islem_ekle(4000, "Yemek", "Gider", "Dışarıda yemek")

    cuzdan.ozet_goster()