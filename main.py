from sh1106_graphics import GraphicsSSD1306
import time

oled = GraphicsSSD1306()  # default 128x64, SDA=21, SCL=22

# Initial positions and velocity
circle_x, circle_y = 30, 30
circle_dx, circle_dy = 1, 1
circle_r = 3

rect_x, rect_y = 60, 10
rect_dx, rect_dy = 1, 1
rect_w, rect_h = 30, 15

while True:
    oled.fill(0)  # clear screen

    # Draw bouncing circle
    oled.fill_circle(circle_x, circle_y, circle_r, 1)
    oled.text("X:",0,0)
    oled.text(str(circle_x),20,0)
    oled.text("Y:",60,0)
    oled.text(str(circle_y),80,0)
    # Draw bouncing rectangle
    #oled.fill_rect(rect_x, rect_y, rect_w, rect_h, 1)

    # Update display
    oled.show()

    # Move circle
    circle_x += circle_dx
    circle_y += circle_dy

    # Bounce circle off edges
    if circle_x - circle_r <= 0 or circle_x + circle_r >= oled.width:
        circle_dx = -circle_dx
    if circle_y - circle_r <= 0 or circle_y + circle_r >= oled.height:
        circle_dy = -circle_dy

    # Move rectangle
    #rect_x += rect_dx
    #rect_y += rect_dy

    # Bounce rectangle off edges
    #if rect_x <= 0 or rect_x + rect_w >= oled.width:
        #rect_dx = -rect_dx
    #if rect_y <= 0 or rect_y + rect_h >= oled.height:
        #rect_dy = -rect_dy

    #time.sleep(0.01)  # 10ms delay → adjust speed
    
    