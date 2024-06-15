from machine import I2C, Pin, UART, PWM # type: ignore
from dht import DHT22 # type: ignore
from libs.machine_i2c_lcd import I2cLcd
import time

# 初始化I2C和LCD
try:
    i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
    time.sleep(1)
    lcd = I2cLcd(i2c, 0x27, 2, 16)
    time.sleep(1)
    lcd.putstr("tspi\nstarting")
except Exception as e:
    print("Error initializing I2C or LCD:", e)

# 初始化UART
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# 初始化舵机
# 黑色舵机
mServo = PWM(Pin(0))
mServo.freq(50)
#右舵机
rServo = PWM(Pin(2))
rServo.freq(50)
#杆舵机
gServo = PWM(Pin(14))
gServo.freq(50)
# 超声波舵机
cServo = PWM(Pin(6))
cServo.freq(50)

# 初始化红外传感器
lInfrared = Pin(10, Pin.IN)
mInfrared = Pin(11, Pin.IN)
rInfrared = Pin(12, Pin.IN)

# LED
led = Pin(13, Pin.OUT)
led.on()

# DHT22
dht=DHT22(Pin(1))
dhtTime = 0

while 1:
    # 读取串口
    time.sleep(0.1)
    rUart = uart.read()
    rUart = str(rUart)
    rUart = (rUart[2:4])
    print(rUart)
    if rUart == "10":
        lcd.clear()
        lcd.putstr("System\nCompleted")
        time.sleep(1)
        break
while 1:
    # 读取串口
    time.sleep(0.1)
    rUart = uart.read()
    rUart = str(rUart)
    rUart = (rUart[2:4])
    print(rUart)
    if rUart == "10":
        lcd.clear()
        lcd.putstr("Connecting      Keyboard")
        time.sleep(1)
    if rUart == "41":
        lcd.clear()
        lcd.putstr("Keyboard        is connected")
        time.sleep(1)
        break
while 1:
    try:
        # 读取串口
        time.sleep(0.1)
        rUart = uart.read()
        rUart = str(rUart)
        rUart = (rUart[2:4])
        print(rUart)
        uart.flush()
        # 舵机
        if rUart == "19":
            mServo.duty_u16(1638)
        if rUart == "33":
            mServo.duty_u16(0)
        if rUart == "47":
            mServo.duty_u16(6553)
        if rUart == "20":
            gServo.duty_u16(2500)
        if rUart == "34":
            gServo.duty_u16(8191)
        if rUart == "21":
            cServo.duty_u16(2500)
        if rUart == "35":
            cServo.duty_u16(8191)

        # led
        if rUart == "38":
            led.off()
        if rUart == "25":
            led.on()

        # IP
        if rUart == "15":
            while 1:
                rUart = uart.read()
                rUart = str(rUart)
                lUart = len(rUart)
                print(rUart)
                print(lUart)
                uart.flush()
                if lUart > 8:
                    break
            rUart = "IP:" + (rUart[2:-5])
            print(rUart)
            lcd.clear()
            lcd.putstr(rUart)
            time.sleep(5)

        # DHT22
        dhtTime =dhtTime + 1
        if dhtTime == 20:
            dht.measure()
            temperature = dht.temperature()
            temperature = str(temperature)
            humidity = dht.humidity()
            humidity = str(humidity)
            text = "T:" + temperature + "C " + "H:" + humidity + "%"
            lcd.clear()
            lcd.putstr(text)
            dhtTime = 0

    except Exception as e:
        print("Error in loop:", e)