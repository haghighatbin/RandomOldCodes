import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)

channel = 0
assert 0 <= channel <= 7

while True:
	request = spi.xfer2([1,(8+channel)<<4,0])
	response = (((request[1]&3) << 8) + request[2]) * 5 / float(1023) 
	print response 
	time.sleep(0.1)

spi.close()
