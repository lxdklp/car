from asyncio import sleep
from machine import I2C, Pin, UART, PWM # type: ignore
from dht import DHT22 # type: ignore
from libs.machine_i2c_lcd import I2cLcd
import time
"""
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
time.sleep(1)
lcd = I2cLcd(i2c, 0x27, 2, 16)
time.sleep(2)
lcd.putstr("tspi\nstarting")
print(2)"""

"""dht=DHT22(Pin(1))
dhtTime = 0
dht.measure()
temperature = dht.temperature()
print(temperature)
humidity = dht.humidity()
print(humidity)"""

"""dj1 = Pin(2,Pin.OUT)
dj2 = Pin(3,Pin.OUT)
dj1.on()
dj2.on()
time.sleep(5)
dj1.off()
dj2.off()"""

"""uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
def Uart():
        time.sleep(0.01)
        rUart = uart.read()
        rUart = str(rUart)
        rUart = (rUart)
        print(rUart)
        uart.flush()
        return (rUart)
while 1:
    print(Uart())
    time.sleep(0.1)"""

lInfrared = Pin(10, Pin.IN)
mInfrared = Pin(11, Pin.IN)
rInfrared = Pin(12, Pin.IN)
print(lInfrared.value())
print(mInfrared.value())
print(rInfrared.value())