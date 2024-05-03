from gpiozero import Motor, PWMOutputDevice
import time

ena = PWMOutputDevice(12)
enb = PWMOutputDevice(13)
motor_a = Motor(forward=17, backward=27)
motor_b = Motor(forward=5, backward=22)


def forward(num, en_value):
    ena.value = en_value
    enb.value = en_value
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

def left(num, en_value):
    ena.value = en_value
    enb.value = en_value
    motor_a.backward()
    motor_b.forward()
    time.sleep(num)
    motor_a.stop()
    motor_b.stop()

def curve_left_while_forward():
    forward(1, 0.5)  # Move forward for 1 second at 50% speed
    left(0.5, 0.5) 
    forward(0.75, 0.5)   # 

curve_left_while_forward()