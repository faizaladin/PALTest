from gpiozero import Motor, PWMOutputDevice
import time

ena = PWMOutputDevice(12)
enb = PWMOutputDevice(13)
motor_a = Motor(forward=17, backward=27)
motor_b = Motor(forward=5, backward=22)

ena.value = 0.5
enb.value = 0.5

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


backward(3)
time.sleep(1)
forward(2)

