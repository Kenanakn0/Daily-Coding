class Araba:
    def __init__(self, marka, renk, beygir):
        self.marka = marka
        self.renk = renk
        self.beygir = beygir
        self.hiz = 0

    def gaza_bas(self):
        self.hiz = self.hiz + 10
        print(f"{self.marka} hızlandı. Şu anki hız: {self.hiz}")

    def bilgi_ver(self):
        print(f"🚗 {self.marka} (Normal) -> Renk: {self.renk} | Güç: {self.beygir} HP | Hız: {self.hiz}")

class Sporaraba(Araba):
    
    def turbo_ac(self):
        self.hiz = self.hiz + 50
        print(f"🚀 {self.marka} TURBOyu açtı! Hız fırladı: {self.hiz}")

    def bilgi_ver(self):
        print(f"🏎️ DİKKAT! Bu bir {self.marka} YARIŞ CANAVARI! | Renk: {self.renk} | Güç: {self.beygir} HP | Hız: {self.hiz}")


# --- TEST KISMI ---

print("--- NORMAL ARABA ---")
normal = Araba("Toyota", "Gri", 100)
normal.bilgi_ver() 
normal.gaza_bas()
normal.bilgi_ver()

print("-" * 30)

print("--- SPOR ARABA ---")
spor = Sporaraba("PORSCHE", "KIRMIZI", 350)
spor.bilgi_ver()
spor.gaza_bas()
spor.turbo_ac()
spor.bilgi_ver()