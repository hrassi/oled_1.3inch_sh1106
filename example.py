from sh1106_graphics import GraphicsSSD1306

oled = GraphicsSSD1306()
oled.fill(0)

# Text
oled.text("Hello OLED", 0, 0)

# Pixel
oled.pixel(10, 15)

# Line
oled.line(0, 20, 127, 20)

# Rectangle
oled.rect(5, 25, 50, 20)

# Filled rectangle
oled.fill_rect(60, 25, 50, 20)

# Circle
oled.circle(100, 40, 15)

# Filled circle
oled.fill_circle(30, 50, 8)



oled.show()
