from gpiozero import Motor, PWMOutputDevice
import time

ena = PWMOutputDevice(12)
enb = PWMOutputDevice(13)
motor_a = Motor(forward=17, backward=27)
motor_b = Motor(forward=5, backward=22)


def forward(num):
    ena.value = 0.25
    enb.value = 0.25
    motor_a.forward()
    motor_b.forward()
    time.sleep(num)
    motor_a.stop()
    motor_b.stop()

def backward(num):
    ena.value = 0.25
    enb.value = 0.25
    motor_a.backward()
    motor_b.backward()
    time.sleep(num)
    motor_a.stop()
    motor_b.stop()

def right(num):
    ena.value = 0.87
    enb.value = 0.87
    motor_a.forward()
    motor_b.backward()
    time.sleep(num)
    motor_a.stop()
    motor_b.stop()

def left(num):
    ena.value = 0.87
    enb.value = 0.87
    motor_a.backward()
    motor_b.forward()
    time.sleep(num)
    motor_a.stop()
    motor_b.stop()

forward(1.5)
time.sleep(1)
left(1.35)
time.sleep(1)

forward(1.5)
time.sleep(1)
left(1.35)
time.sleep(1)

forward(1.5)
time.sleep(1)
left(1.35)
time.sleep(1)

forward(1.5)
time.sleep(1)
left(1.35)
time.sleep(1)


