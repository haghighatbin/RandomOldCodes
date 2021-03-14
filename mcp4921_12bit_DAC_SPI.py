import spidev
import sys

spi = spidev.SpiDev()
spi.open(0,1)

in_val = int(float(sys.argv[1]) * 4095 / 5)
assert 0 <= in_val <= 4096, 'The input voltage has to be a value between 0 to 5 V'

spi.xfer2([((15 & 3) << 4) + ((in_val & 0xF00) >> 8), (in_val & 0x0FF)])

spi.close()
