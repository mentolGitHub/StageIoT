from machine import UART
import pycom
import time



pycom.heartbeat(False)
# this uses the UART_1 default pins for TXD and RXD (``P3`` and ``P4``)
print("starting 1..")
pycom.rgbled(0x010100)
uart = UART(1, baudrate=9600)
buf = ""

while 1 :
    uart.write('test')   # write the 3 charactersà^)
    print(uart.read(uart.any()))
    time.sleep(2)