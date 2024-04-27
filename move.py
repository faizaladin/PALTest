from gpiozero import Motor, PWMOutputDevice
import time

ena = PWMOutputDevice(12)
enb = PWMOutputDevice(13)
motor_a = Motor(forward=17, backward=27)
motor_b = Motor(forward=5, backward=22)

ena.value = 1.0
enb.value = 1.0

def forward(num):
    motor_a.forward()
    motor_b.forward()
    time.sleep(num)
    motor_a.stop()
    motor_b.stop()

forward(2)
