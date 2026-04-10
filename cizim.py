import turtle
import random

tosba = turtle.Turtle()
tosba.speed(0)
tosba.pensize(2)

def kare_ciz(buyukluk):
    for i in range(4):
        tosba.forward(buyukluk)
        tosba.right(90)

colors = ["red","blue","green","yellow","purple","orange" 
          ,"pink","brown","gray","cyan"]
for i in range(36):
    tosba.color(random.choice(colors))

    kare_ciz(100)

    tosba.right(10)
turtle.done()