# main.py -- put your code here!
import pyb
from st import SensorTile
from pyb import Timer, Pin, ExtInt, RTC
from micropython import const
import baticon

SLEEPCNT = const(10)
SW_PIN = 'PG11'
VUSB_PIN = 'PG10'

st = SensorTile()

from machine import I2C
i2c=machine.I2C(-1, sda=machine.Pin("C1"), scl=machine.Pin("C0"), freq=400000)  

from ssd1306 import SSD1306_I2C
oled = SSD1306_I2C(128, 64, i2c)

oled.framebuf.rect(0,0,127,63,1)
oled.msg('Pocket',40,8)
oled.msg('Watch',44,28)
oled.text('MPY SensorTile', 8, 48)
oled.show()
pyb.delay(1000)
oled.fill(0)
oled.show()

flag = 1
sleepcnt = SLEEPCNT
keypressed = 0
keycnt = 0
page = 0

def rtcisr(t):
    pyb.LED(1).toggle()
    return
    
rtc=RTC()
rtc.init()
rtc.wakeup(1000, rtcisr)

def tmisr(t):
    global flag
    flag = 1

tm = Timer(1, freq=1, callback=tmisr)

'''def puts(s, x, y):
    oled.framebuf.fill_rect(x, y, 8*len(s), 8, 0)
    oled.text(s, x, y)
'''
def show_bat():
    oled.puts('%4.2fV'%st.BatVolt(), 16, 56)
    oled.puts('%2d'%sleepcnt, 112, 56)
    oled.show()

def show_press(page):
    if(page==0):
        oled.puts('%8.3f'%st.P(), 64, 0)
    elif(page==1):
        oled.msg('%8.3f'%st.P(), 48, 20)
        oled.msg("%5.1fC"%st.T(), 72, 36)

def show_temp():
    oled.puts("%5.1fC"%st.T(), 64, 56)

def show_accel(page):
    if(page==0):
        oled.puts("%7.2f"%st.AX(), 64, 8)
        oled.puts("%7.2f"%st.AY(), 64, 16)
        oled.puts("%7.2f"%st.AZ(), 64, 24)
    elif(page==2):
        oled.msg("%7.2f"%st.AX(), 56, 0)
        oled.msg("%7.2f"%st.AY(), 56, 16)
        oled.msg("%7.2f"%st.AZ(), 56, 32)

def show_gyro(page):
    if(page==0):
        oled.puts("%7.2f"%st.GX(), 64, 32)
        oled.puts("%7.2f"%st.GY(), 64, 40)
        oled.puts("%7.2f"%st.GZ(), 64, 48)
    elif(page==3):
        oled.msg("%7.2f"%st.GX(), 56, 0)
        oled.msg("%7.2f"%st.GY(), 56, 16)
        oled.msg("%7.2f"%st.GZ(), 56, 32)
    
    
def show_title(page):
    oled.fill(0)    # clear screen
    if(page==1):
        oled.msg("Press", 0, 0)
    elif(page==2):
        oled.msg("Accel", 0, 0)
    elif(page==3):
        oled.msg("Gyro", 0, 0)
    else:
        oled.puts("Press:", 0, 0)
        oled.puts("Accel:", 0, 8)
        oled.puts("Gyro:", 0, 32)

def swisr(t):
    global keypressed
    keypressed = 1
    #print('.')

def showbaticon(n, x, y):
    if(n > 10):
        n = 10
    if(n < 0):
        n = 0
    for i in range(16):
        d = baticon.font[n*16+i]
        for j in range(8):
            oled.pixel(x+i, y+7-j, d&(1<<j))

sw = pyb.ExtInt(SW_PIN, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback=swisr)
btn = pyb.Pin(SW_PIN, pyb.Pin.IN, pull=pyb.Pin.PULL_UP)
vusb = pyb.Pin(VUSB_PIN, pyb.Pin.IN, pull=pyb.Pin.PULL_NONE)

batc = st.Bat()
def showbat():
    global batc
    if(vusb()):
        batc = batc + 1
        if(batc > 10):
            batc = st.Bat()
    else:
        batc = st.Bat()
    showbaticon(batc, 0, 56)
    oled.puts('%4.2fV'%st.BatVolt(), 16, 56)

show_title(page)
while True:
    if(flag):
        flag = 0
        
        # keypressed
        if(keypressed):
            keypressed = 0
            sleepcnt = SLEEPCNT
            page = (page + 1)%4
            show_title(page)


        if(btn()==0):
            keycnt = keycnt + 1
            if(keycnt > 3):
                machine.soft_reset()            
        else:
            keycnt = 0

        #show sensor
        show_press(page)
        show_accel(page)
        show_gyro(page)
        show_temp()
        
        #show battery
        showbat()
        
        #power save
        if(vusb()==0):
            if(sleepcnt>0):
                sleepcnt = sleepcnt - 1
            else:
                oled.poweroff()
                while True:
                    machine.idle()
                    #machine.sleep()
                    if(btn()==0):
                        break;
                oled.poweron()
                sleepcnt = SLEEPCNT
            oled.puts('%2d'%sleepcnt, 112, 56)
        else:
            oled.puts('  ', 112, 56)

        oled.show()

