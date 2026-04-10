class Sporaraba(Araba):
    
    def turbo_ac(self):
        self.hiz_self =self.hiz + 50

        print(f"{self.marka} turbo modu açıldı.Şu anki hız:{self.hiz_self}")

spor_araba1=Sporaraba("PORSCHE","KIRMIZI",350)

norma_araba=Araba("TOYOTA","MAVİ",200)
print("-"*30)

norma_araba.gaza_bas()

spor_araba1.gaza_bas()

spor_araba1.turbo_ac()
