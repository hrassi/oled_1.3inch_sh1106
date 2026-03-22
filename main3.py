from sh1106_graphics import GraphicsSSD1306
import time
oled = GraphicsSSD1306()  # default 128x64, SDA=21, SCL=22


oled.fill(0)  # clear screen
oled.line(0,10,128,10,1)
oled.show()   #Update display

y=0 
n=128
x=0
speed=1
while True:
    oled.text("Oled Screen",n+speed,0,y)
    oled.text("Oled Screen",n,y,1)
    page = y // 8
    oled.show_page(page) # refresh only the scroling line
    n=n-speed
    if n< -100:
        n=128
        x=x+1
        oled.text("Counter: ",5,55,1)
        oled.fill_rect(70,55,40,10,0)
        
        oled.text(str(x),70,55,1)
        oled.show()