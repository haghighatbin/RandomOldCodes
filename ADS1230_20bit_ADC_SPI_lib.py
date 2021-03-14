#/bin/usr
import spidev
	
class ADS1230:
	
	def __init__(self, VDD, spi_bus, spi_CS):
		
		self.spi = spidev.SpiDev()
		self.spi.open(spi_bus, spi_CS)
		self.VDD = VDD
	
	def read_ads1230(self):

		dummy_bytes = self.spi.xfer2([0, 0, 0])
		resp = (((dummy_bytes[0] & 0x7F) << 16) + (dummy_bytes[1] << 8)
		 + (dummy_bytes[2] & 0xF0)) * self.VDD / float(524287)
		return resp
		

