from gpiozero import Motor, PWMOutputDevice
import time

ena = PWMOutputDevice(12)
enb = PWMOutputDevice(13)
motor_a = Motor(forward=17, backward=27)
motor_b = Motor(forward=5, backward=22)

ena.value = 0.25
enb.value = 0.25

def forward(num):
    motor_a.forward()
    motor_b.forward()
    time.sleep(num)
    motor_a.stop()
    motor_b.stop()

def backward(num):
    motor_a.backward()
    motor_b.backward()
    time.sleep(num)
    motor_a.stop()
    motor_b.stop()

def left(num):
    motor_a.forward()
    motor_b.backward()
    time.sleep(num)
    motor_a.stop()
    motor_b.stop()

def right(num):
    motor_a.backward()
    motor_b.forward()
    time.sleep(num)
    motor_a.stop()
    motor_b.stop()

forward(2)
time.sleep(1)
left(2)
time.sleep(1)
right(2)
time.sleep(1)
backward(2)

