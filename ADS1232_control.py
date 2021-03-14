#!/usr/bin/env python
"""
DVDD, AVDD, RefP >> VDD
DGND, CLKIN, Gain, RefN, AGND, Speed, AINN1-2, XTAL1-2 >> GND
CAPS >> connected to each other with a 220 nF cap (bridged)
AINP >> I'm using a a simple Light-dependent resistor(LDR) to provide an analog signal
DRDY/DOUT >> MISO
MOSI unconnected
SCLK >> SCLK
A0 >> GND reads AINP1 ---- A0 >> 
"""
import ADS1232_24bit_ADC_SPI_lib as ads
import RPi.GPIO as GPIO
import time

import spidev
spi = spidev.SpiDev()
spi_bus = 0
spi_CS = 0

VDD = 3.3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


Gain_Pin_0 = 22
Gain_Pin_1 = 23
PWDN_Pin = 24
Temp_Pin = 27
Speed_Pin = 18
time_read = 0.5 # sampling intervals

GPIO.setup(PWDN_Pin, GPIO.OUT)
GPIO.setup(Gain_Pin_0, GPIO.OUT)
GPIO.setup(Gain_Pin_1, GPIO.OUT)
GPIO.setup(Temp_Pin, GPIO.OUT)
GPIO.setup(Speed_Pin, GPIO.OUT)

#def temperature_read():
	
	#try:
		#while True:
			#resp = ads.ADS1232(spi.bus, spi.CS)
			#resp = resp.read_temp()
			#print resp
			#time.sleep(time_read)
		
	#finally:
		#GPIO.output(PWDN_Pin, GPIO.LOW)
		#GPIO.output(Temp_Pin, GPIO.LOW)
		#GPIO.cleanup()
		#spi.close()	

def signal_read():
	
	try:
		while True:
			resp = ads.ADS1232(VDD, spi_bus, spi_CS)
			resp = resp.read_ads1232()
			print resp
			time.sleep(time_read)
		
	finally:
		GPIO.output(PWDN_Pin, GPIO.LOW)
		GPIO.output(Gain_Pin_0, GPIO.LOW)
		GPIO.output(Gain_Pin_1, GPIO.LOW)
		GPIO.output(Temp_Pin, GPIO.LOW)
		GPIO.output(Speed_Pin, GPIO.LOW)
		GPIO.cleanup()
		spi.close()

def main(switch, speed, gain, temp):
	
	if 	temp == 'disable':
		print "Temperature pin is disabled!"
		GPIO.output(Temp_Pin, GPIO.LOW)
		
	elif temp == 'enable':
		print "Temperature pin is enabled!"
		GPIO.output(Temp_Pin, GPIO.HIGH)
		#temperature_read():
			
		
	if switch == 'on':
		print "Switch pin is in HIGH status"
		GPIO.output(PWDN_Pin, GPIO.HIGH)
	elif switch == 'off':
		print "Switch pin is in LOW status"
		GPIO.output(PWDN_Pin, GPIO.LOW)
		
	if  speed == 1:
		print "Speed pin is in HIGH status"
		GPIO.output(Speed_Pin, GPIO.HIGH) # speed 1 : 80 SPS
	elif switch == 'off':
		print "Speed pin is in LOW status"
		GPIO.output(Speed_Pin, GPIO.LOW) # speed 0 : 10 SPS
				
	if gain == 1:
		print "Gain = 0"
		GPIO.output(Gain_Pin_0, GPIO.LOW)
		GPIO.output(Gain_Pin_1, GPIO.LOW)
	elif gain == 2:
		print "Gain = 1"
		GPIO.output(Gain_Pin_0, GPIO.HIGH)
		GPIO.output(Gain_Pin_1, GPIO.LOW)
	elif gain == 64:
		print "Gain = 64"
		GPIO.output(Gain_Pin_0, GPIO.LOW)
		GPIO.output(Gain_Pin_1, GPIO.HIGH)
	elif gain == 128:
		print "Gain = 128"
		GPIO.output(Gain_Pin_0, GPIO.HIGH)
		GPIO.output(Gain_Pin_1, GPIO.HIGH)
	print "VDD = %f" % VDD	+ "\n"
	
	signal_read()


if __name__ == "__main__":
	
	switch = 'on' # or 'off'
	gain = 1 # gain values: [1, 2, 64, 128]
	temp = 'disable' # or 'enable'
	speed = 0 
	main(switch, gain, temp)
