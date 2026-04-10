print("NOT HESAPLAYICI PROGRAMINA HOŞGELDİNİZ")

vize = int(input("lütfen vize notu giriniz:"))
final = int(input("lütfen final notu giriniz:"))


ortalama = (vize *0.4) + (final *0.6)

print("Not otalamanız :", ortalama)

if ortalama >=90:
    print("AA aldınız")

elif ortalama >=85:
    print("BA aldınız")
 
elif ortalama >=80:
    print("BB aldınız")
elif ortalama <=50:
    print("dersten kaldınız")