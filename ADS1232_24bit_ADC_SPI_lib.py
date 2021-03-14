#!/usr/bin/env python
import spidev
	
class ADS1232:
	
	
	def __init__(self, VCC, spi_bus = 0, spi_CS = 0):
		
		self.spi = spidev.SpiDev()
		self.spi.open(spi_bus, spi_CS)
		self.VCC = VCC
		
	def read_ads1232(self):

		dummy_bytes = self.spi.xfer2([0, 0, 0])
		resp = (((dummy_bytes[0] & 0x7F) << 16) + (dummy_bytes[1] << 8)
		 + (dummy_bytes[2])) * self.VCC / float(8388607)
		return resp
	
	def read_temp(self):
		pass
		
		

