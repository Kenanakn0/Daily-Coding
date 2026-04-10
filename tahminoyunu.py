import random
print("--Sayı Tahmin Oyununa Hoşgeldiniz--")
print("1 - 100 arasında bir sayı tutum ,yiyorsa gel de bul 😂")

gizli_sayı = random.randint(1,100)

deneme_sayısı = 0

while True:
    tahmin = int(input("Tahminin Nedir? : "))
    deneme_sayısı = deneme_sayısı + 1

    if tahmin < gizli_sayı:
        print("Daha bükük bir sayı söyle! 🔼")

    elif tahmin > gizli_sayı:
        print("Daha küçük bir sayı söyle! 🔽")

    else:
        print("-"*30)
        print("Tebrikler! Syısıyı Bildin 🎉")
        print(f"Toplam {deneme_sayısı} denemede buldunç")

        break 