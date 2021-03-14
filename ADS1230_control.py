#!/usr/bin/env python
"""
DVDD, AVDD, RefP >> VDD
DGND, CLKIN, Gain, RefN, AGND, Speed, AINN >> GND
CAPS >> connected to each other with a 220 nF cap (bridged)
AINP >> I'm using a a simple Light-dependent resistor(LDR) to provide an analog signal
DRDY/DOUT >> MISO
MOSI unconnected
SCLK >> SCLK
"""
import ADS1230_20bit_ADC_SPI_lib as ads
import RPi.GPIO as GPIO
import time

import spidev
spi = spidev.SpiDev()
spi_bus = 0
spi_CS = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

VDD = 3.3

Gain_Pin = 23
PWDN_Pin = 24
Speed_Pin = 18 
time_read = 0.5 # sampling intervals

GPIO.setup(PWDN_Pin, GPIO.OUT)
GPIO.setup(Gain_Pin, GPIO.OUT)
GPIO.setup(Speed_Pin, GPIO.OUT)

def main(switch, speed, gain):
	
	if switch == 'on':
		GPIO.output(PWDN_Pin, GPIO.HIGH)
	elif switch == 'off':
		GPIO.output(PWDN_Pin, GPIO.LOW)
	
	if speed == 0: # speed 0 : 10 SPS
		GPIO.output(Speed_Pin, GPIO.LOW)
	elif speed == 1: # speed 1 : 80 SPS
		GPIO.output(Speed_Pin, GPIO.HIGH)
				
	if gain == 0: # gain 0 : pga 64
		GPIO.output(Gain_Pin, GPIO.LOW)
	elif gain == 1: # gain 1 : pga 128
		GPIO.output(Gain_Pin, GPIO.HIGH)
		
	signal_read()

def signal_read():
	
	try:
		while True:
			resp = ads.ADS1230(VDD, spi_bus, spi_CS)
			resp = resp.read_ads1230()
			print resp
			time.sleep(time_read)
		
	finally:
		GPIO.output(PWDN_Pin, GPIO.LOW)
		GPIO.output(Gain_Pin, GPIO.LOW)
		GPIO.output(Speed_Pin, GPIO.LOW)
		GPIO.cleanup()
		spi.close()

if __name__ == "__main__":
	switch = 'on'
	speed = 0
	gain = 0 
	main(switch, speed, gain)
