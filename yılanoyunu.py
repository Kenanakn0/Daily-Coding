import turtle
import time
import random

delay = 0.1  


pencere = turtle.Screen()
pencere.title("Python Yılan Oyunu")
pencere.bgcolor("black")
pencere.setup(width=600, height=600)
pencere.tracer(0) 


kafa = turtle.Turtle()
kafa.speed(0)
kafa.shape("square")
kafa.color("white")
kafa.penup()
kafa.goto(0, 0)
kafa.direction = "stop"

# --- 3. YEMEK ---
yemek = turtle.Turtle()
yemek.speed(0)
yemek.shape("circle")
yemek.color("red")
yemek.penup()
yemek.goto(0, 100)


kuyruklar = [] 
puan = 0


yazi = turtle.Turtle()
yazi.speed(0)
yazi.color("white")
yazi.penup()
yazi.hideturtle()
yazi.goto(0, 260)
yazi.write("Puan: 0", align="center", font=("Courier", 24, "normal"))

def yukari():
    if kafa.direction != "down": 
        kafa.direction = "up"

def asagi():
    if kafa.direction != "up":
        kafa.direction = "down"

def sola():
    if kafa.direction != "right":
        kafa.direction = "left"

def saga():
    if kafa.direction != "left":
        kafa.direction = "right"

def hareket():
    if kafa.direction == "up":
        y = kafa.ycor() 
        kafa.sety(y + 20) 
    
    if kafa.direction == "down":
        y = kafa.ycor()
        kafa.sety(y - 20)
    
    if kafa.direction == "left":
        x = kafa.xcor()
        kafa.setx(x - 20)
    
    if kafa.direction == "right":
        x = kafa.xcor()
        kafa.setx(x + 20)


pencere.listen()
pencere.onkey(yukari, "w")  
pencere.onkey(asagi, "s")   
pencere.onkey(sola, "a")    
pencere.onkey(saga, "d")   


while True:
    pencere.update() 

    
    if kafa.xcor() > 290 or kafa.xcor() < -290 or kafa.ycor() > 290 or kafa.ycor() < -290:
        time.sleep(1)
        kafa.goto(0, 0)
        kafa.direction = "stop"
        
        
        for parca in kuyruklar:
            parca.goto(1000, 1000) 
        kuyruklar.clear()
        
      
        puan = 0
        yazi.clear()
        yazi.write("Puan: {}".format(puan), align="center", font=("Courier", 24, "normal"))

    
    if kafa.distance(yemek) < 20:
        
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        yemek.goto(x, y)

    
        yeni_kuyruk = turtle.Turtle()
        yeni_kuyruk.speed(0)
        yeni_kuyruk.shape("square")
        yeni_kuyruk.color("grey")
        yeni_kuyruk.penup()
        kuyruklar.append(yeni_kuyruk)

       
        puan = puan + 10
        yazi.clear()
        yazi.write("Puan: {}".format(puan), align="center", font=("Courier", 24, "normal"))

   
    for i in range(len(kuyruklar) - 1, 0, -1):
        x = kuyruklar[i-1].xcor()
        y = kuyruklar[i-1].ycor()
        kuyruklar[i].goto(x, y)
    
   
    if len(kuyruklar) > 0:
        x = kafa.xcor()
        y = kafa.ycor()
        kuyruklar[0].goto(x, y)

    hareket() 

    
    for parca in kuyruklar:
        if parca.distance(kafa) < 20:
            time.sleep(1)
            kafa.goto(0, 0)
            kafa.direction = "stop"
            
           
            for parca in kuyruklar:
                parca.goto(1000, 1000)
            kuyruklar.clear()
            puan = 0
            yazi.clear()
            yazi.write("Puan: 0", align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)