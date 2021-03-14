#/bin/usr
import RPi.GPIO as GPIO
import binascii
import spidev
import time
GPIO.setwarnings(False)

spi = spidev.SpiDev()
spi.open(0,0)
#spi.open(0,1)
spi.mode = 1
#spi.cshigh = True
#spi.lsbfirst = False

PWDN = 24
Gain_pin = 23
Gain = 0
switch = 'on'

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
                        response = spi.xfer2([0,0,0])
                        print (((response[0]&0x07)<<16) + (response[1] << 8) + (response[2]&0xFF))  * 5 / float(524287)
                        time.sleep(1)
        finally:
                GPIO.output(PWDN, GPIO.LOW)
                GPIO.cleanup()
                spi.close()

if __name__ == '__main__':
        main()
