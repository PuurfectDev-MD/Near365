import time

_CMD_TIMEOUT = const(100)
_R1_IDLE_STATE = const(1 << 0)
_R1_ILLEGAL_COMMAND = const(1 << 2)
_TOKEN_CMD25 = const(0xfc)
_TOKEN_STOP_TRAN = const(0xfd)
_TOKEN_DATA = const(0xfe)

class SDCard:
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.cmdbuf = bytearray(6)
        self.dummybuf = bytearray(512)
        for i in range(512):
            self.dummybuf[i] = 0xff
        self.dummybuf_memoryview = memoryview(self.dummybuf)
        self.init_card()

    def init_spi(self, baudrate):
        try:
            self.spi.init(baudrate=baudrate, phase=0, polarity=0)
        except TypeError:
            self.spi.init()

    def init_card(self):
        self.cs.init(self.cs.OUT, value=1)
        self.init_spi(100000)
        for i in range(16):
            self.spi.write(b'\xff')
        for _ in range(5):
            if self.cmd(0, 0, 0x95) == _R1_IDLE_STATE:
                break
        else:
            raise OSError("no SD card")
        r = self.cmd(8, 0x01aa, 0x87, 4)
        if r == _R1_IDLE_STATE:
            self.init_card_v2()
        elif r == (_R1_IDLE_STATE | _R1_ILLEGAL_COMMAND):
            self.init_card_v1()
        else:
            raise OSError("couldn't determine SD card version")
        if self.cmd(9, 0, 0, 0, False) != 0:
            raise OSError("no response from SD card")
        csd = bytearray(16)
        self.readinto(csd)
        if csd[0] & 0xc0 != 0x40:
            raise OSError("SD card CSD format not supported")
        self.sectors = ((csd[8] << 8 | csd[9]) + 1) * 1024
        if self.cmd(16, 512, 0) != 0:
            raise OSError("can't set 512 block size")
        self.init_spi(1320000)

    def init_card_v1(self):
        for i in range(_CMD_TIMEOUT):
            self.cmd(55, 0, 0)
            if self.cmd(41, 0, 0) == 0:
                self.cdv = 512
                return
        raise OSError("timeout waiting for v1 card")

    def init_card_v2(self):
        for i in range(_CMD_TIMEOUT):
            time.sleep_ms(50)
            self.cmd(58, 0, 0, 4)
            self.cmd(55, 0, 0)
            try:
                if self.cmd(41, 0x40000000, 0) == 0:
                    self.cmd(58, 0, 0, 4)
                    self.cdv = 1
                    return
            except OverflowError:
                if self.cmd(41, 0x4000000, 0) == 0:
                    self.cmd(58, 0, 0, 4)
                    self.cdv = 1
                    return
        raise OSError("timeout waiting for v2 card")

    def cmd(self, cmd, arg, crc, final=0, release=True):
        self.cs.value(0)
        buf = self.cmdbuf
        buf[0] = 0x40 | cmd
        buf[1] = arg >> 24
        buf[2] = arg >> 16
        buf[3] = arg >> 8
        buf[4] = arg
        buf[5] = crc
        self.spi.write(buf)
        for i in range(_CMD_TIMEOUT):
            response = self.spi.read(1, 0xff)[0]
            if not (response & 0x80):
                if final:
                    self.spi.readinto(self.cmdbuf[:final])
                if release:
                    self.cs.value(1)
                    self.spi.write(b'\xff')
                return response
        self.cs.value(1)
        self.spi.write(b'\xff')
        return 1

    def readinto(self, buf):
        self.cs.value(0)
        while self.spi.read(1, 0xff)[0] != 0xfe:
            pass
        self.spi.readinto(buf)
        self.spi.read(2, 0xff)
        self.cs.value(1)
        self.spi.write(b'\xff')

    def write(self, token, buf):
        self.cs.value(0)
        self.spi.write(bytes([token]))
        self.spi.write(buf)
        self.spi.write(b'\xff\xff')
        if (self.spi.read(1, 0xff)[0] & 0x1f) != 0x05:
            self.cs.value(1)
            self.spi.write(b'\xff')
            return
        while self.spi.read(1, 0xff)[0] == 0x00:
            pass
        self.cs.value(1)
        self.spi.write(b'\xff')

    def count(self):
        return self.sectors

    def readblocks(self, block_num, buf):
        nblocks, err = divmod(len(buf), 512)
        assert nblocks and not err, 'Buffer length is invalid'
        if nblocks == 1:
            if self.cmd(17, block_num * self.cdv, 0, release=False) != 0:
                self.cs.value(1)
                self.spi.write(b'\xff')
                return 1
            self.readinto(buf)
        else:
            if self.cmd(18, block_num * self.cdv, 0, release=False) != 0:
                self.cs.value(1)
                self.spi.write(b'\xff')
                return 1
            offset = 0
            mv = memoryview(buf)
            while nblocks:
                self.readinto(mv[offset : offset + 512])
                offset += 512
                nblocks -= 1
            self.cmd(12, 0, 0xff)
        return 0

    def writeblocks(self, block_num, buf):
        nblocks, err = divmod(len(buf), 512)
        assert nblocks and not err, 'Buffer length is invalid'
        if nblocks == 1:
            if self.cmd(24, block_num * self.cdv, 0, release=False) != 0:
                self.cs.value(1)
                self.spi.write(b'\xff')
                return 1
            self.write(_TOKEN_DATA, buf)
        else:
            if self.cmd(25, block_num * self.cdv, 0, release=False) != 0:
                self.cs.value(1)
                self.spi.write(b'\xff')
                return 1
            offset = 0
            mv = memoryview(buf)
            while nblocks:
                self.write(_TOKEN_CMD25, mv[offset : offset + 512])
                offset += 512
                nblocks -= 1
            self.write(_TOKEN_STOP_TRAN, b'')
        return 0