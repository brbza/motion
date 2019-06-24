import machine


class MPU6050(object):
    SELF_TEST_X = 0x0D
    SELF_TEST_Y = 0x0E
    SELF_TEST_Z = 0x0F
    SELF_TEST_A = 0x10
    SMPLRT_DIV = 0x19
    CONFIG = 0x1A
    GYRO_CONFIG = 0x1B
    ACCEL_CONFIG = 0x1C
    FIFO_EN = 0x23
    I2C_MST_CTRL = 0x24
    I2C_SLV0_ADDR = 0x25
    I2C_SLV0_REG = 0x26
    I2C_SLV0_CTRL = 0x27
    I2C_SLV1_ADDR = 0x28
    I2C_SLV1_REG = 0x29
    I2C_SLV1_CTRL = 0x2A
    I2C_SLV2_ADDR = 0x2B
    I2C_SLV2_REG = 0x2C
    I2C_SLV2_CTRL = 0x2D
    I2C_SLV3_ADDR = 0x2E
    I2C_SLV3_REG = 0x2F
    I2C_SLV3_CTRL = 0x30
    I2C_SLV4_ADDR = 0x31
    I2C_SLV4_REG = 0x32
    I2C_SLV4_DO = 0x33
    I2C_SLV4_CTRL = 0x34
    I2C_SLV4_DI = 0x35
    I2C_MST_STATUS = 0x36
    INT_PIN_CFG = 0x37
    INT_ENABLE = 0x38
    INT_STATUS = 0x3A
    ACCEL_XOUT_H = 0x3B
    ACCEL_XOUT_L = 0x3C
    ACCEL_YOUT_H = 0x3D
    ACCEL_YOUT_L = 0x3E
    ACCEL_ZOUT_H = 0x3F
    ACCEL_ZOUT_L = 0x40
    TEMP_OUT_H = 0x41
    TEMP_OUT_L = 0x42
    GYRO_XOUT_H = 0x43
    GYRO_XOUT_L = 0x44
    GYRO_YOUT_H = 0x45
    GYRO_YOUT_L = 0x46
    GYRO_ZOUT_H = 0x47
    GYRO_ZOUT_L = 0x48
    EXT_SENS_DATA_00 = 0x49
    EXT_SENS_DATA_01 = 0x4A
    EXT_SENS_DATA_02 = 0x4B
    EXT_SENS_DATA_03 = 0x4C
    EXT_SENS_DATA_04 = 0x4D
    EXT_SENS_DATA_05 = 0x4E
    EXT_SENS_DATA_06 = 0x4F
    EXT_SENS_DATA_07 = 0x50
    EXT_SENS_DATA_08 = 0x51
    EXT_SENS_DATA_09 = 0x52
    EXT_SENS_DATA_10 = 0x53
    EXT_SENS_DATA_11 = 0x54
    EXT_SENS_DATA_12 = 0x55
    EXT_SENS_DATA_13 = 0x56
    EXT_SENS_DATA_14 = 0x57
    EXT_SENS_DATA_15 = 0x58
    EXT_SENS_DATA_16 = 0x59
    EXT_SENS_DATA_17 = 0x5A
    EXT_SENS_DATA_18 = 0x5B
    EXT_SENS_DATA_19 = 0x5C
    EXT_SENS_DATA_20 = 0x5D
    EXT_SENS_DATA_21 = 0x5E
    EXT_SENS_DATA_22 = 0x5F
    EXT_SENS_DATA_23 = 0x60
    I2C_SLV0_DO = 0x63
    I2C_SLV1_DO = 0x64
    I2C_SLV2_DO = 0x65
    I2C_SLV3_DO = 0x66
    I2C_MST_DELAY_CTRL = 0x67
    SIGNAL_PATH_RESET = 0x68
    USER_CTRL = 0x6A
    PWR_MGMT_1 = 0x6B
    PWR_MGMT_2 = 0x6C
    FIFO_COUNTH = 0x72
    FIFO_COUNTL = 0x73
    FIFO_R_W = 0x74
    WHO_AM_I = 0x75

    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.iic.start()
        self.iic.writeto(self.addr, bytearray([107, 0]))
        self.iic.stop()

    def _session(self):
        self.iic.start()
        yield
        self.iic.stop()

    def _read_from_mem(self, address, num_bytes):
        self._session()
        return self.iic.readfrom_mem(self.addr, address, num_bytes)

    def _write_to_mem(self, address, values):
        self._session()
        self.iic.writeto_mem(self.addr, address, values)

    def get_raw_values(self):
        self.iic.start()
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        self.iic.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        vals = {}
        vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
        vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
        vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
        vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
        vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
        vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        return vals  # returned in range of Int16
        # -32768 to 32767

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            print(self.get_values())
            sleep(0.05)
