from machine import I2C, Pin, UART, PWM # type: ignore
from dht import DHT22 # type: ignore
from libs.machine_i2c_lcd import I2cLcd
import time

# 初始化I2C和LCD
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
time.sleep(1)
lcd = I2cLcd(i2c, 0x27, 2, 16)
time.sleep(1)
lcd.putstr("tspi\nstarting")

# 初始化UART
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# 初始化舵机
# 黑色舵机
mServo = PWM(Pin(0))
mServo.freq(50)
#右舵机
rServo = PWM(Pin(13))
rServo.freq(50)
#左舵机
lServo = PWM(Pin(14))
lServo.freq(50)
# 超声波舵机
cServo = PWM(Pin(6))
cServo.freq(50)
c = 20

# 初始化红外传感器
lInfrared = Pin(10, Pin.IN)
mInfrared = Pin(11, Pin.IN)
rInfrared = Pin(12, Pin.IN)
infrared = 5

# LED
led = Pin(7, Pin.OUT)
led.on()
led2 = Pin(25, Pin.OUT)
led2.on()

# DHT22
dht=DHT22(Pin(1))
dhtTime = 20

# 主电机
dj1 = Pin(2,Pin.OUT)
dj2 = Pin(3,Pin.OUT)
dj1.off()
dj2.off()

# 串口通信
def Uart():
        time.sleep(0.01)
        rUart = uart.read()
        rUart = str(rUart)
        rUart = (rUart[2:4])
        print(rUart)
        uart.flush()
        return (rUart)
# 等待泰山派启动
while 1:
    if Uart() == "10":
        lcd.clear()
        lcd.putstr("System\nCompleted")
        time.sleep(1)
        break
while 1:
    if Uart() == "10":
        lcd.clear()
        lcd.putstr("Connecting      Keyboard")
        time.sleep(1)
    if Uart() == "41":
        lcd.clear()
        lcd.putstr("Keyboard        is connected")
        time.sleep(1)
        break

while 1:
    # 电机
    if Uart() == "17":
        dj1.on()
        dj2.on()
        while 1:
            if Uart() != "17" or mInfrared.value() == 0:
                dj1.off()
                dj2.off()
                break
    if Uart() == "30":
        dj1.on()
        while 1:
            if Uart() != "30" or rInfrared.value() == 0:
                dj1.off()
                break
    if Uart() == "32":
        dj2.on()
        while 1:
            if Uart() != "32" or lInfrared.value() == 0:
                dj2.off()
                break
    # 舵机
    if Uart() == "19":
        mServo.duty_u16(1638)
    if Uart() == "33":
        mServo.duty_u16(0)
    if Uart() == "47":
        mServo.duty_u16(6553)
    if Uart() == "20":
        mServo.duty_u16(1638)
    if Uart() == "34":
        mServo.duty_u16(0)
    if Uart() == "48":
        mServo.duty_u16(6553)
    if Uart() == "21":
        mServo.duty_u16(1638)
    if Uart() == "35":
        mServo.duty_u16(0)
    if Uart() == "49":
        mServo.duty_u16(6553)
    # 超声波
    if c == 20:
        cServo.duty_u16(2500)
    if c == 40:
        cServo.duty_u16(8191)
        c =0
    c = c + 1


    # led
    if Uart() == "38":
        led.toggle()

    # IP
    if Uart() == "15":
        while 1:
            time.sleep(0.01)
            iUart = uart.read()
            iUart = str(iUart)
            lUart = len(iUart)
            print(iUart)
            print(lUart)
            uart.flush()
            if lUart > 8:
                break
        iUart = "IP:" + (iUart[2:-11])
        print(iUart)
        lcd.clear()
        lcd.putstr(iUart)
        time.sleep(5)

    # DHT22
    if dhtTime == 20:
        dht.measure()
        temperature = dht.temperature()
        temperature = str(temperature)
        humidity = dht.humidity()
        humidity = str(humidity)
        dhtText = "T:" + temperature + "C " + "H:" + humidity + "%"
        dhtTime = 0
    dhtTime =dhtTime + 1

    # 红外传感器
    infraredText = "L:" + str(lInfrared.value()) + " M: " + str(mInfrared.value()) + " R: " + str(rInfrared.value())
    infrared = 0
    if not (lInfrared.value() and mInfrared.value() and rInfrared.value()):
        lcd.backlight_off()
        time.sleep(0.5)
        lcd.backlight_on()

    # keyboard check
    if Uart() == "10":
        lcd.clear()
        lcd.putstr("Keyboard        Disconnected")

    # LCD更新
    text = dhtText + " " + infraredText
    lcd.clear()
    lcd.putstr(text)