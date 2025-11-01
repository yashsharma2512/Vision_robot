from machine import Pin, UART
import time, ujson


# === UART Setup ===
uart = UART(0, baudrate=921600, tx=Pin(0), rx=Pin(1))

# === Motor Setup ===
IN1 = Pin(10, Pin.OUT)
IN2 = Pin(11, Pin.OUT)
IN3 = Pin(13, Pin.OUT)
IN4 = Pin(12, Pin.OUT)


def stop():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)


def forward():
    IN1.value(1)
    IN2.value(0)
    IN3.value(1)
    IN4.value(0)


def backward():
    IN1.value(0)
    IN2.value(1)
    IN3.value(0)
    IN4.value(1)


def left():
    IN1.value(0)
    IN2.value(1)
    IN3.value(1)
    IN4.value(0)


def right():
    IN1.value(1)
    IN2.value(0)
    IN3.value(0)
    IN4.value(1)


while True:
    forward()
    time.sleep(1)
    stop()
    time.sleep(1)
    #uncomment 
#     left()
#     time.sleep(1)
#     right()
#     time.sleep(1)
        