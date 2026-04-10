import turtle
import random
import time

ekran = turtle.Screen()
ekran.setup(width=600 , height=500)
ekran.title("Büyük Kamplumbağ Yarışı")
ekran.bgcolor("lightgreen")

çizgi_kalemi = turtle.Turtle()
çizgi_kalemi.penup
çizgi_kalemi.goto(230,200)
çizgi_kalemi.pendown
çizgi_kalemi.pensize(5)
çizgi_kalemi.right(90)
çizgi_kalemi.forward(400)
çizgi_kalemi.hideturtle()

renkler = ["red","blue","green","orange","purple"]
yaris_pistindeki_tosbalar = []

y_konumu = -100

for renk in renkler:
    yeni_tosba = turtle.Turtle()
    yeni_tosba.shape("turtle")
    yeni_tosba.color(renk)
    yeni_tosba.penup()

    yeni_tosba.goto(-230,y_konumu)

    yaris_pistindeki_tosbalar.append(yeni_tosba)

kullanicidan_tahmin = ekran.textinput("Tahmin", "Hangi renk kazanacak? (red, blue, green, orange, purple): ")

if kullanicidan_tahmin:
    yarıs_devam_ediyor = True
else:
    yarıs_devam_ediyor = False

while yarıs_devam_ediyor:
    for tosba in yaris_pistindeki_tosbalar:
        rastgele_ilerleme = random.randint(1,10)
        tosba.forward(rastgele_ilerleme)

        if tosba.xcor() > 220:
            yarıs_devam_ediyor = False
            kazanan_renk = tosba.pencolor()
            if kazanan_renk == kullanicidan_tahmin:
                print(f"Tebrikler! Kazanan renk: {kazanan_renk}")
            else:
                print(f"Üzgünüm, kazanan renk: {kazanan_renk}. Tekrar deneyin!")

                time.sleep(0.05)
                
            break 