import framebuf

_SET_CONTRAST        = 0x81
_SET_NORM_INV        = 0xa6
_SET_DISP            = 0xae
_SET_MEM_ADDR        = 0x20
_SET_COL_ADDR        = 0x21
_SET_PAGE_ADDR       = 0x22
_SET_DISP_START_LINE = 0x40
_SET_SEG_REMAP       = 0xa0
_SET_MUX_RATIO       = 0xa8
_SET_COM_OUT_DIR     = 0xc0
_SET_DISP_OFFSET     = 0xd3
_SET_COM_PIN_CFG     = 0xda
_SET_DISP_CLK_DIV    = 0xd5
_SET_PRECHARGE       = 0xd9
_SET_VCOM_DESEL      = 0xdb
_SET_CHARGE_PUMP     = 0x8d

class SH1106_I2C(framebuf.FrameBuffer):
    def __init__(self, width, height, i2c, addr=0x3c):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)

        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)

        self.init_display()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([0x80, cmd]))

    def write_data(self, buf):
        self.i2c.writeto(self.addr, b'\x40' + buf)

    def init_display(self):
        for cmd in (
            _SET_DISP | 0x00,
            _SET_MEM_ADDR, 0x00,
            _SET_DISP_START_LINE | 0x00,
            _SET_SEG_REMAP | 0x01,
            _SET_MUX_RATIO, 0x3f,
            _SET_COM_OUT_DIR | 0x08,
            _SET_DISP_OFFSET, 0x00,
            _SET_COM_PIN_CFG, 0x12,
            _SET_DISP_CLK_DIV, 0x80,
            _SET_PRECHARGE, 0xf1,
            _SET_VCOM_DESEL, 0x30,
            _SET_CONTRAST, 0xff,
            _SET_NORM_INV,
            _SET_CHARGE_PUMP, 0x14,
            _SET_DISP | 0x01,
        ):
            self.write_cmd(cmd)

        self.fill(0)
        self.show()

    def show(self):
        for page in range(self.pages):
            self.write_cmd(0xb0 + page)
            self.write_cmd(0x02)
            self.write_cmd(0x10)
            start = self.width * page
            end = start + self.width
            self.write_data(self.buffer[start:end])
            