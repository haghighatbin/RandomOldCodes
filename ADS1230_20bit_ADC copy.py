#/bin/usr
import RPi.GPIO as GPIO
import spidev
import time
#GPIO.setwarnings(False)

"""
DVDD, AVDD, RefP >> 5 V
DGND, CLKIN, Gain, RefN, AGND, Speed, AINN >> GND
CAPS >> connected to each other with a 220 nF cap (bridged)
AINP >> I'm using a a simple Light-dependent resistor(LDR) to provide an analog signal
DRDY/DOUT >> MISO
MOSI unconnected
SCLK >> SCLK
"""

spi = spidev.SpiDev()
spi.open(0, 0)
spi.mode = 1

PWDN = 24
Gain_pin = 23
Gain = 1  # [Gain 0 / PGA 64 ----- Gain 1 / PGA 128]
switch = 'on'
time_read = 0.3

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWDN, GPIO.OUT)
GPIO.setup(Gain_pin, GPIO.OUT)

if switch == 'on':            
        GPIO.output(PWDN, GPIO.HIGH)
elif switch == 'off':
        GPIO.output(PWDN, GPIO.LOW)

if Gain == 0:            
        GPIO.output(Gain_pin, GPIO.LOW)
elif Gain == 1:
        GPIO.output(Gain_pin, GPIO.HIGH)


def main():
        try:
                
                while True:
                        response = spi.xfer2([0, 0, 0])
                        print(((response[0] & 0x07) << 16) + (response[1] << 8) + (response[2] & 0xFF)) * 5 / float(524287)
                        time.sleep(time_read)
        finally:
                GPIO.output(PWDN, GPIO.LOW)
                GPIO.cleanup()
                spi.close()

if __name__ == '__main__':
        main()
