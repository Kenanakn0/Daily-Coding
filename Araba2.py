class Arabalar:
    def __init__(self,marka,renk,beygir):
        self.marka=marka
        self.renk=renk
        self.beygir=beygir
        self.hiz=0

    def gaza_bas(self):
            self.hiz=self.hiz +10
            print(f"{self.marka} hızlandı.Şu anki hız:{self.hiz}")

    def frene_bas(self):
            self.hiz=self.hiz -10
            print(f"{self.marka} yavaşladı.Şu anki hızı:{self.hiz}") 
            
            if self.hiz<0:
                self.hiz=0
                print(F"{self.marka} Araba zaten duruyor.Hız negatif olamaz.")

    def bilgi_ver(self):
            print(f" {self.marka} marka araba.Rengi:{self.renk}.Gücü:{self.beygir}")

           

araba1=Arabalar("Ferari","SİYAH",300)
araba2=Arabalar("Tofaş","BEYAZ",100)

araba1.bilgi_ver()
araba2.bilgi_ver()

print("-"*30)

araba1.gaza_bas()
araba2.frene_bas()

print(f"Tofaş'ın hızı:{araba2.hiz}")


        