# ssd1306_graphics.py
# Graphics wrapper for SSD1306 OLED for MicroPython (ESP32)

from machine import Pin, I2C
import sh1106
from micropython import const

__version__ = "0.2"

class GraphicsSSD1306:
    def __init__(self, width=128, height=64, i2c=None, scl_pin=22, sda_pin=21, addr=const(0x3C)):
        """
        Initialize the OLED display.
        - width, height: OLED resolution
        - i2c: optional I2C object; if None, it's created automatically
        - scl_pin, sda_pin: default GPIO22/21
        - addr: I2C address (usually 0x3C)
        """
        if i2c is None:
            i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)
        self.oled = sh1106.SH1106_I2C(width, height, i2c, addr)
        self.width = width
        self.height = height

    # Basic display methods
    def fill(self, color=0):
        self.oled.fill(color)

    def show(self):
        self.oled.show()
        
    def show_page(self, page):

        self.oled.write_cmd(0xB0 + page)
        self.oled.write_cmd(0x02)
        self.oled.write_cmd(0x10)

        start = page * self.oled.width
        end = start + self.oled.width

        self.oled.write_data(self.oled.buffer[start:end])

    def pixel(self, x, y, col=1):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.oled.pixel(x, y, col)

    def text(self, txt, x, y, col=1):
        self.oled.text(txt, x, y, col)

    # Lines and rectangles
    def line(self, x0, y0, x1, y1, col=1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            self.pixel(x0, y0, col)
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def rect(self, x, y, w, h, col=1):
        self.line(x, y, x + w, y, col)
        self.line(x + w, y, x + w, y + h, col)
        self.line(x + w, y + h, x, y + h, col)
        self.line(x, y + h, x, y, col)

    def fill_rect(self, x, y, w, h, col=1):
        """
        Draw a filled rectangle.
        - x, y: top-left corner
        - w, h: width and height
        - col: color (1=white, 0=black)
        """
        for i in range(y, y + h):
            self.line(x, i, x + w, i, col)

    # Circle
    def circle(self, x0, y0, r, col=1):
        x = r
        y = 0
        err = 0
        while x >= y:
            self.pixel(x0 + x, y0 + y, col)
            self.pixel(x0 + y, y0 + x, col)
            self.pixel(x0 - y, y0 + x, col)
            self.pixel(x0 - x, y0 + y, col)
            self.pixel(x0 - x, y0 - y, col)
            self.pixel(x0 - y, y0 - x, col)
            self.pixel(x0 + y, y0 - x, col)
            self.pixel(x0 + x, y0 - y, col)
            y += 1
            if err <= 0:
                err += 2 * y + 1
            if err > 0:
                x -= 1
                err -= 2 * x + 1

    # Filled circle
    def fill_circle(self, x0, y0, r, col=1):
        for ry in range(-r, r + 1):
            for rx in range(-r, r + 1):
                if rx * rx + ry * ry <= r * r:
                    self.pixel(x0 + rx, y0 + ry, col)

