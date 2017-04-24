"""
  File:     ST.py
  Descipt:  ST SensorTile kit module, sensors drive and basic function 
  Author:   Shaoziyang
  Version:  1.0
  DATE:     2017.2
  home:     http://www.micropython.org.cn/

  usage:

"""
import pyb
import machine
from machine import Pin, I2C

__author__ = "shaoziyang <shaoziyang@outlook.com>"
__version__ = "1.0.0" 
__info__ = 'micropython module for SensorTile kit'
        
#pin
LPS22HB_CS_PIN = 'PA3'
LSM6DSM_CS_PIN = 'PB12'
LSM303AGR_CS_A_PIN = 'PC4'
LSM303AGR_CS_M_PIN = 'PB1'
VBAT_PIN = 'PC2'
SW_PIN = 'PG11'

# LPS22HB register
LPS22HB_ADDRESS = const(0x5D)
LPS22HB_INTERRUPT_CFG= const(0x0B)
LPS22HB_THS_P_L      = const(0x0C)
LPS22HB_THS_P_H      = const(0x0D)
LPS22HB_WHO_AM_I     = const(0x0F)
LPS22HB_CTRL_REG1    = const(0x10)
LPS22HB_CTRL_REG2    = const(0x11)
LPS22HB_CTRL_REG3    = const(0x12)
LPS22HB_FIFO_CTRL    = const(0x14)
LPS22HB_REF_P_XL     = const(0x15)
LPS22HB_REF_P_L      = const(0x16)
LPS22HB_REF_P_H      = const(0x17)
LPS22HB_RPDS_L       = const(0x18)
LPS22HB_RPDS_H       = const(0x19)
LPS22HB_RES_CONF     = const(0x1A)
LPS22HB_INT_SOURCE   = const(0x25)
LPS22HB_FIFO_STATUS  = const(0x26)
LPS22HB_STATUS       = const(0x27)
LPS22HB_PRESS_OUT_XL = const(0x28)
LPS22HB_PRESS_OUT_L  = const(0x29)
LPS22HB_PRESS_OUT_H  = const(0x2A)
LPS22HB_TEMP_OUT_L   = const(0x2B)
LPS22HB_TEMP_OUT_H   = const(0x2C)
LPS22HB_LPFP_RES     = const(0x33)

# LSM6DSM register
LSM6DSM_ADDRESS = const(0x6B)
LSM6DSM_FUNC_CFG_ACCESS = const(0x01)
LSM6DSM_SENSOR_SYNC_TIME_FRAME= const(0x04)
LSM6DSM_SENSOR_SYNC_RES_RATIO = const(0x05)
LSM6DSM_FIFO_CTRL1   = const(0x06)
LSM6DSM_FIFO_CTRL2   = const(0x07)
LSM6DSM_FIFO_CTRL3   = const(0x08)
LSM6DSM_FIFO_CTRL4   = const(0x09)
LSM6DSM_FIFO_CTRL5   = const(0x0A)
LSM6DSM_DRDY_PULSE_CFG=const(0x0B)
LSM6DSM_INT1_CTRL    = const(0x0D)
LSM6DSM_INT2_CTRL    = const(0x0E)
LSM6DSM_WHO_AM_I     = const(0x0F)
LSM6DSM_CTRL1_XL     = const(0x10)
LSM6DSM_CTRL2_G      = const(0x11)
LSM6DSM_CTRL3_C      = const(0x12)
LSM6DSM_CTRL4_C      = const(0x13)
LSM6DSM_CTRL5_C      = const(0x14)
LSM6DSM_CTRL6_C      = const(0x15)
LSM6DSM_CTRL7_G      = const(0x16)
LSM6DSM_CTRL8_XL     = const(0x17)
LSM6DSM_CTRL9_XL     = const(0x18)
LSM6DSM_CTRL10_C     = const(0x19)
LSM6DSM_MASTER_CONFIG= const(0x1A)
LSM6DSM_WAKE_UP_SRC  = const(0x1B)
LSM6DSM_TAP_SRC      = const(0x1C)
LSM6DSM_D6D_SRC      = const(0x1D)
LSM6DSM_STATUS_REG   = const(0x1E)
LSM6DSM_OUT_TEMP_L   = const(0x20)
LSM6DSM_OUT_TEMP_H   = const(0x21)
LSM6DSM_OUTX_L_G     = const(0x22)
LSM6DSM_OUTX_H_G     = const(0x23)
LSM6DSM_OUTY_L_G     = const(0x24)
LSM6DSM_OUTY_H_G     = const(0x25)
LSM6DSM_OUTZ_L_G     = const(0x26)
LSM6DSM_OUTZ_H_G     = const(0x27)
LSM6DSM_OUTX_L_XL    = const(0x28)
LSM6DSM_OUTX_H_XL    = const(0x29)
LSM6DSM_OUTY_L_XL    = const(0x2A)
LSM6DSM_OUTY_H_XL    = const(0x2B)
LSM6DSM_OUTZ_L_XL    = const(0x2C)
LSM6DSM_OUTZ_H_XL    = const(0x2D)
LSM6DSM_SENSORHUB1_REG=const(0x2E)
LSM6DSM_SENSORHUB2_REG=const(0x2F)
LSM6DSM_SENSORHUB3_REG=const(0x30)
LSM6DSM_SENSORHUB4_REG=const(0x31)
LSM6DSM_SENSORHUB5_REG=const(0x32)
LSM6DSM_SENSORHUB6_REG=const(0x33)
LSM6DSM_SENSORHUB7_REG=const(0x34)
LSM6DSM_SENSORHUB8_REG=const(0x35)
LSM6DSM_SENSORHUB9_REG=const(0x36)
LSM6DSM_SENSORHUB10_REG = const(0x37)
LSM6DSM_SENSORHUB11_REG = const(0x38)
LSM6DSM_SENSORHUB12_REG = const(0x39)
LSM6DSM_FIFO_STATUS1 = const(0x3A)
LSM6DSM_FIFO_STATUS2 = const(0x3B)
LSM6DSM_FIFO_STATUS3 = const(0x3C)
LSM6DSM_FIFO_STATUS4 = const(0x3D)
LSM6DSM_FIFO_DATA_OUT_L = const(0x3E)
LSM6DSM_FIFO_DATA_OUT_H = const(0x3F)
LSM6DSM_TIMESTAMP0_REG  = const(0x40)
LSM6DSM_TIMESTAMP1_REG  = const(0x41)
LSM6DSM_TIMESTAMP2_REG  = const(0x42)
LSM6DSM_STEP_TIMESTAMP_L= const(0x49)
LSM6DSM_STEP_TIMESTAMP_H= const(0x4A)
LSM6DSM_STEP_COUNTER_L  = const(0x4B)
LSM6DSM_STEP_COUNTER_H  = const(0x4C)
LSM6DSM_SENSORHUB13_REG = const(0x4D)
LSM6DSM_SENSORHUB14_REG = const(0x4E)
LSM6DSM_SENSORHUB15_REG = const(0x4F)
LSM6DSM_SENSORHUB16_REG = const(0x50)
LSM6DSM_SENSORHUB17_REG = const(0x51)
LSM6DSM_SENSORHUB18_REG = const(0x52)
LSM6DSM_FUNC_SRC1    = const(0x53)
LSM6DSM_FUNC_SRC2    = const(0x54)
LSM6DSM_WRIST_TILT_IA= const(0x55)
LSM6DSM_TAP_CFG      = const(0x58)
LSM6DSM_TAP_THS_6D   = const(0x59)
LSM6DSM_INT_DUR2     = const(0x5A)
LSM6DSM_WAKE_UP_THS  = const(0x5B)
LSM6DSM_WAKE_UP_DUR  = const(0x5C)
LSM6DSM_FREE_FALL    = const(0x5D)
LSM6DSM_MD1_CFG      = const(0x5E)
LSM6DSM_MD2_CFG      = const(0x5F)
LSM6DSM_MASTER_CMD_CODE = const(0x60)
LSM6DSM_SENS_SYNC_SPI_ERROR_CODE = const(0x61)
LSM6DSM_OUT_MAG_RAW_X_L = const(0x66)
LSM6DSM_OUT_MAG_RAW_X_H = const(0x67)
LSM6DSM_OUT_MAG_RAW_Y_L = const(0x68)
LSM6DSM_OUT_MAG_RAW_Y_H = const(0x69)
LSM6DSM_OUT_MAG_RAW_Z_L = const(0x6A)
LSM6DSM_OUT_MAG_RAW_Z_H = const(0x6B)
LSM6DSM_INT_OIS      = const(0x6F)
LSM6DSM_CTRL1_OIS    = const(0x70)
LSM6DSM_CTRL2_OIS    = const(0x71)
LSM6DSM_CTRL3_OIS    = const(0x72)
LSM6DSM_X_OFS_USR    = const(0x73)
LSM6DSM_Y_OFS_USR    = const(0x74)
LSM6DSM_Z_OFS_USR    = const(0x75)

# LSM303AGR
LSM303AGR_ADDRESS_A  = const(0x19)
LSM303AGR_ADDRESS_M  = const(0x1E)
LSM303AGR_STATUS_REG_AUX_A = const(0x07)
LSM303AGR_OUT_TEMP_L_A=const(0x0C)
LSM303AGR_OUT_TEMP_H_A=const(0x0D)
LSM303AGR_INT_COUNTER_REG_A = const(0x0E)
LSM303AGR_WHO_AM_I_A = const(0x0F)
LSM303AGR_TEMP_CFG_REG_A = const(0x1F)
LSM303AGR_CTRL_REG1_A= const(0x20)
LSM303AGR_CTRL_REG2_A= const(0x21)
LSM303AGR_CTRL_REG3_A= const(0x22)
LSM303AGR_CTRL_REG4_A= const(0x23)
LSM303AGR_CTRL_REG5_A= const(0x24)
LSM303AGR_CTRL_REG6_A= const(0x25)
LSM303AGR_REFERENCE  = const(0x26)
LSM303AGR_STATUS_REG_A=const(0x27)
LSM303AGR_OUT_X_L_A  = const(0x28)
LSM303AGR_OUT_X_H_A  = const(0x29)
LSM303AGR_OUT_Y_L_A  = const(0x2A)
LSM303AGR_OUT_Y_H_A  = const(0x2B)
LSM303AGR_OUT_Z_L_A  = const(0x2C)
LSM303AGR_OUT_Z_H_A  = const(0x2D)
LSM303AGR_FIFO_CTRL_REG_A= const(0x2E)
LSM303AGR_FIFO_SRC_REG_A = const(0x2F)
LSM303AGR_INT1_CFG_A = const(0x30)
LSM303AGR_INT1_SRC_A = const(0x31)
LSM303AGR_INT1_THS_A = const(0x32)
LSM303AGR_INT1_DURATION_A= const(0x33)
LSM303AGR_INT2_CFG_A = const(0x34)
LSM303AGR_INT2_SRC_A = const(0x35)
LSM303AGR_INT2_THS_A = const(0x36)
LSM303AGR_INT2_DURATION_A= const(0x37)
LSM303AGR_CLICK_CFG_A= const(0x38)
LSM303AGR_CLICK_SRC_A= const(0x39)
LSM303AGR_CLICK_THS_A= const(0x3A)
LSM303AGR_TIME_LIMIT_A=const(0x3B)
LSM303AGR_TIME_LATENCY_A = const(0x3C)
LSM303AGR_TIME_WINDOW_A  = const(0x3D)
LSM303AGR_Act_THS_A  = const(0x3E)
LSM303AGR_Act_DUR_A  = const(0x3F)
LSM303AGR_OFFSET_X_REG_L_M = const(0x45)
LSM303AGR_OFFSET_X_REG_H_M = const(0x46)
LSM303AGR_OFFSET_Y_REG_L_M = const(0x47)
LSM303AGR_OFFSET_Y_REG_H_M = const(0x48)
LSM303AGR_OFFSET_Z_REG_L_M = const(0x49)
LSM303AGR_OFFSET_Z_REG_H_M = const(0x4A)
LSM303AGR_WHO_AM_I_M = const(0x4F)
LSM303AGR_CFG_REG_A_M= const(0x60)
LSM303AGR_CFG_REG_B_M= const(0x61)
LSM303AGR_CFG_REG_C_M= const(0x62)
LSM303AGR_INT_CRTL_REG_M   = const(0x63)
LSM303AGR_INT_SOURCE_REG_M = const(0x64)
LSM303AGR_INT_THS_L_REG_M  = const(0x65)
LSM303AGR_INT_THS_H_REG_M  = const(0x66)
LSM303AGR_STATUS_REG_M=const(0x67)
LSM303AGR_OUTX_L_REG_M=const(0x68)
LSM303AGR_OUTX_H_REG_M=const(0x69)
LSM303AGR_OUTY_L_REG_M=const(0x6A)
LSM303AGR_OUTY_H_REG_M=const(0x6B)
LSM303AGR_OUTZ_L_REG_M=const(0x6C)
LSM303AGR_OUTZ_H_REG_M=const(0x6D)

BATVTAB = (3450, 3560, 3680, 3770, 3850, 3920, 3980, 4040, 4100, 4180)

def pd(dat):
    if(dat > 0x7FFF):
        dat -= 65536
    return dat

class SensorTile(object):
    def __init__(self):
        # set CS high
        CS_LPS22HB = Pin(LPS22HB_CS_PIN, Pin.OUT)
        CS_LPS22HB(1)
        CS_AG = Pin(LSM6DSM_CS_PIN, Pin.OUT)
        CS_AG(1)
        CS_A = Pin(LSM303AGR_CS_A_PIN, Pin.OUT)
        CS_A(1)
        CS_M = Pin(LSM303AGR_CS_M_PIN, Pin.OUT)
        CS_M(1)

        # soft I2C
        self.i2c = machine.I2C(-1, sda=machine.Pin('PB15'), scl=machine.Pin('PB13'))
        # set open drain and pull up
        sda=machine.Pin('PB15', Pin.OPEN_DRAIN, pull=Pin.PULL_UP)
        scl=machine.Pin('PB13', Pin.OPEN_DRAIN, pull=Pin.PULL_UP)
        
        # start LPS22HB
        self.setreg(0x18, LPS22HB_CTRL_REG1, LPS22HB_ADDRESS)
        self.temp0 = 0
        self.press = 0
        self.LPS22HB_ON = True
        
        # start LSM6DSM
        self.setreg(0x6C, LSM6DSM_CTRL1_XL, LSM6DSM_ADDRESS)
        self.setreg(0x68, LSM6DSM_CTRL2_G, LSM6DSM_ADDRESS)
        self.temp1 = 0
        self.ax1 = self.ay1 = self.az1 = 0
        self.gx = self.gy = self.gz = 0
        self.LSM6DSM_A_ON = True
        self.LSM6DSM_G_ON = True

        # start LSM303AGR
        self.setreg(0x6F, LSM303AGR_CTRL_REG1_A, LSM303AGR_ADDRESS_A)
        self.setreg(0x80, LSM303AGR_CTRL_REG4_A, LSM303AGR_ADDRESS_A)
        self.setreg(0x00, LSM303AGR_CFG_REG_A_M, LSM303AGR_ADDRESS_M)
        self.ax2 = self.ay2 = self.az2 = 0
        self.temp2 = 0
        self.mx = self.my = self.mz = 0
        self.LSM303AGR_A_ON = True
        self.LSM303AGR_M_ON = True
        
        # VBat
        self.vbat = pyb.ADC(Pin(VBAT_PIN))

        # info
        self.ver = '1.0.0'
        self.author = 'shaoziyang <shaoziyang@outlook.com>'
        self.info = 'micropython module for SensorTile kit'
        
    def setreg(self, dat, reg, addr):
        buf = bytearray(2)
        buf[0] = reg
        buf[1] = dat
        self.i2c.writeto(addr, buf)

    def getreg(self, reg, addr):
        buf = bytearray(1)
        buf[0] = reg
        self.i2c.writeto(addr, buf)
        t = self.i2c.readfrom(addr, 1)
        return t[0]

    def get2reg(self, reg, addr):
        l = self.getreg(reg, addr)
        h = self.getreg(reg+1, addr)
        return l+h*256

    # LPS22HB
    def LPS22HB_poweron(self):
        t = self.getreg(LPS22HB_CTRL_REG1, LPS22HB_ADDRESS) & 0x0F
        self.setreg(t|0x10, LPS22HB_CTRL_REG1, LPS22HB_ADDRESS)
        self.LPS22HB_ON = True

    def LPS22HB_poweroff(self):
        t = self.getreg(LPS22HB_CTRL_REG1, LPS22HB_ADDRESS) & 0x0F
        self.setreg(t, LPS22HB_CTRL_REG1, LPS22HB_ADDRESS)
        self.LPS22HB_ON = False
        
    def LPS22HB_temp(self):
        self.temp0 = self.get2reg(LPS22HB_TEMP_OUT_L, LPS22HB_ADDRESS)
        return pd(self.temp0)/100

    def LPS22HB_press(self):
        self.press = self.getreg(LPS22HB_PRESS_OUT_XL, LPS22HB_ADDRESS)
        self.press += self.get2reg(LPS22HB_PRESS_OUT_L, LPS22HB_ADDRESS) * 256
        return self.press/4096

    def LPS22HB(self):
        return [self.LPS22HB_temp(), self.LPS22HB_press()]

    # LSM6DSM
    def LSM6DSM_temp(self):
        self.temp1 = self.get2reg(LSM6DSM_OUT_TEMP_L, LSM6DSM_ADDRESS)
        return 25 + pd(self.temp1)/256

    def LSM6DSM_ax(self):
        self.ax1 = self.get2reg(LSM6DSM_OUTX_L_XL, LSM6DSM_ADDRESS)
        return pd(self.ax1)*0.244

    def LSM6DSM_ay(self):
        self.ay1 = self.get2reg(LSM6DSM_OUTY_L_XL, LSM6DSM_ADDRESS)
        return pd(self.ay1)*0.244

    def LSM6DSM_az(self):
        self.az1 = self.get2reg(LSM6DSM_OUTZ_L_XL, LSM6DSM_ADDRESS)
        return pd(self.az1)*0.244

    def LSM6DSM_a(self):
        return [self.LSM6DSM_ax(), self.LSM6DSM_ay(), self.LSM6DSM_az()]

    def LSM6DSM_a_poweron(self):
        self.setreg(0x6C, LSM6DSM_CTRL1_XL, LSM6DSM_ADDRESS)
        self.LSM6DSM_A_ON = True

    def LSM6DSM_a_poweroff(self):
        self.setreg(0x0C, LSM6DSM_CTRL1_XL, LSM6DSM_ADDRESS)
        self.LSM6DSM_A_ON = False

    def LSM6DSM_gx(self):
        self.gx = self.get2reg(LSM6DSM_OUTX_L_G, LSM6DSM_ADDRESS)
        return pd(self.gx)*0.035

    def LSM6DSM_gy(self):
        self.gy = self.get2reg(LSM6DSM_OUTY_L_G, LSM6DSM_ADDRESS)
        return pd(self.gy)*0.035

    def LSM6DSM_gz(self):
        self.gz = self.get2reg(LSM6DSM_OUTZ_L_G, LSM6DSM_ADDRESS)
        return pd(self.gz)*0.035

    def LSM6DSM_g(self):
        return [self.LSM6DSM_gx(), self.LSM6DSM_gy(), self.LSM6DSM_gz()]

    def LSM6DSM_g_poweron(self):
        self.setreg(0x68, LSM6DSM_CTRL2_G, LSM6DSM_ADDRESS)
        self.LSM6DSM_M_ON = True

    def LSM6DSM_g_poweroff(self):
        self.setreg(0x08, LSM6DSM_CTRL2_G, LSM6DSM_ADDRESS)
        self.LSM6DSM_M_ON = False

    # LSM303AGR
    def LSM303AGR_temp(self):
        self.temp2 = self.get2reg(LSM303AGR_OUT_TEMP_L_A, LSM303AGR_ADDRESS_A)
        return 24 + (pd(self.temp2)//128)/2

    def LSM303AGR_ax(self):
        self.ax2 = self.get2reg(LSM303AGR_OUT_X_L_A, LSM303AGR_ADDRESS_A)
        return pd(self.ax2)*2000/256/128

    def LSM303AGR_ay(self):
        self.ay2 = self.get2reg(LSM303AGR_OUT_Y_L_A, LSM303AGR_ADDRESS_A)
        return pd(self.ay2)*2000/256/128

    def LSM303AGR_az(self):
        self.az2 = self.get2reg(LSM303AGR_OUT_Z_L_A, LSM303AGR_ADDRESS_A)
        return pd(self.az2)*2000/256/128

    def LSM303AGR_a(self):
        return [self.LSM303AGR_ax(), self.LSM303AGR_ay(), self.LSM303AGR_az()]

    def LSM303AGR_a_poweron(self):
        self.setreg(0x6F, LSM303AGR_CTRL_REG1_A, LSM303AGR_ADDRESS_A)
        self.LSM303AGR_A_ON = True

    def LSM303AGR_a_poweroff(self):
        self.setreg(0x0F, LSM303AGR_CTRL_REG1_A, LSM303AGR_ADDRESS_A)
        self.LSM303AGR_A_ON = False

    def LSM303AGR_mx(self):
        self.mx = self.get2reg(LSM303AGR_OUTX_L_REG_M, LSM303AGR_ADDRESS_M)
        return pd(self.mx)

    def LSM303AGR_my(self):
        self.my = self.get2reg(LSM303AGR_OUTY_L_REG_M, LSM303AGR_ADDRESS_M)
        return pd(self.my)

    def LSM303AGR_mz(self):
        self.mz = self.get2reg(LSM303AGR_OUTZ_L_REG_M, LSM303AGR_ADDRESS_M)
        return pd(self.mz)

    def LSM303AGR_m(self):
        return [self.LSM303AGR_mx(), self.LSM303AGR_my(), self.LSM303AGR_mz()]

    def LSM303AGR_m_poweron(self):
        self.setreg(0x00, LSM303AGR_CFG_REG_A_M, LSM303AGR_ADDRESS_M)
        self.LSM303AGR_M_ON = True

    def LSM303AGR_m_poweroff(self):
        self.setreg(0x03, LSM303AGR_CFG_REG_A_M, LSM303AGR_ADDRESS_M)
        self.LSM303AGR_M_ON = False

    # SensorTile
    def MX(self):
        return self.LSM303AGR_mx()

    def MY(self):
        return self.LSM303AGR_my()

    def MZ(self):
        return self.LSM303AGR_mz()

    def M(self):
        return self.LSM303AGR_m()

    def M_ON(self, on = True):
        if(on):
            self.LSM303AGR_m_poweron()
        else:
            self.LSM303AGR_m_poweroff()

    def AX(self):
        return -self.LSM303AGR_ay()

    def AY(self):
        return self.LSM303AGR_ax()

    def AZ(self):
        return self.LSM303AGR_az()

    def A(self):
        return [self.AX(), self.AY(), self.AZ()]

    def A_ON(self, on = True):
        if(on):
            self.LSM303AGR_a_poweron()
        else:
            self.LSM303AGR_a_poweroff()

    def AHX(self):
        return -self.LSM6DSM_ax()

    def AHY(self):
        return self.LSM6DSM_ay()
    
    def AHZ(self):
        return self.LSM6DSM_az()

    def AH(self):
        return [self.AHX(), self.AHY(), self.AHZ()]

    def AH_ON(self, on = True):
        if(on):
            self.LSM6DSM_a_poweron()
        else:
            self.LSM6DSM_a_poweroff()

    def GX(self):
        return self.LSM6DSM_gx()

    def GY(self):
        return self.LSM6DSM_gy()

    def GZ(self):
        return self.LSM6DSM_gz()

    def G(self):
        return self.LSM6DSM_g()

    def G_ON(self, on = True):
        if(on):
            self.LSM6DSM_g_poweron()
        else:
            self.LSM6DSM_g_poweroff()

    def P(self):
        return self.LPS22HB_press()

    def T(self):
        if(self.LPS22HB_ON):
            return self.LPS22HB_temp()
        elif(self.LSM6DSM_ON):
            return self.LSM6DSM_temp()
        elif(self.LSM303AGR_ON):
            return self.LSM303AGR_temp()
        else:
            return 0

    def P_ON(self, on = True):
        if(on):
            self.LPS22HB_poweron()
        else:
            self.LPS22HB_poweroff()

    def ALL(self):
        return [[self.P(), self.T()], self.A(), self.AH(), self.G(), self.M()]

    def BatVolt(self):
        return self.vbat.read() * 8.25 / 4096
    
    def Bat(self):
        for i in range(10):
            if(self.BatVolt()*1000 < BATVTAB[i]):
                break
        return i