import smbus

bus = 1
dev_addr = 0x62
DAC_reg = 0x40

DAC_EEPROM_reg = 0x60
input_V = 3


class mcp4725(object):

    def __init__(self, dev_addr, bus):

        self.smbus = smbus.SMBus(bus)
        self.dev_addr = dev_addr

    def set_voltage(self, value, EEPROM = False):

        if value > 3.3:
            value = 3.3

        if value < 0:
            value = 0
        value = int(float(value) * 4095 / 3.3)
        sending_bytes = [(value >> 4) & 0xFF, (value << 4) & 0xF0]

        if EEPROM:
            self.write_reg(DAC_EEPROM_reg, sending_bytes)

        else:
            self.write_reg(DAC_reg, sending_bytes)
            
    def write_reg(self, reg, sending_bytes):
        self.smbus.write_i2c_block_data(self.dev_addr, reg, sending_bytes)

def main():
    dac = mcp4725(dev_addr, bus)
    dac.set_voltage(input_V, False)

if __name__ == '__main__':
    main()
