from gpiozero import Motor, PWMOutputDevice
import time

ena = PWMOutputDevice(12)
enb = PWMOutputDevice(13)
motor_a = Motor(forward=17, backward=27)
motor_b = Motor(forward=5, backward=22)

def stop():
    motor_a.stop()
    motor_b.stop()

def forward(num, en_value):
    ena.value = en_value
    enb.value = en_value
    motor_a.forward()
    motor_b.forward()
    time.sleep(num)

def backward(num):
    ena.value = 0.25
    enb.value = 0.25
    motor_a.backward()
    motor_b.backward()
    time.sleep(num)

def right(num):
    ena.value = 0.87
    enb.value = 0.87
    motor_a.forward()
    motor_b.backward()
    time.sleep(num)

def left(num, en_value):
    ena.value = en_value
    enb.value = en_value
    motor_a.backward()
    motor_b.forward()
    time.sleep(num)

def curve_left_while_forward125():
    forward(0.25, 0.5)  # Move forward for 1 second at 50% speed
    left(1.2, 1) 
    forward(1, 0.5)   # 
    stop()

def curve_left_while_forward250():
    forward(0.25, 0.5)  # Move forward for 1 second at 50% speed
    left(1.05, 1) 
    forward(1, 0.5)   # 
    stop()

def curve_left_while_forward375():
    forward(0.25, 0.5)  # Move forward for 1 second at 50% speed
    left(0.95, 1) 
    forward(1, 0.5)   # 
    stop()

def curve_left_while_forward500():
    forward(0.25, 0.5)  # Move forward for 1 second at 50% speed
    left(0.80, 1) 
    forward(1, 0.5)   # 
    stop()

def curve_left_while_forward625():
    forward(0.25, 0.5)  # Move forward for 1 second at 50% speed
    left(0.65, 1) 
    forward(1, 0.5)   # 
    stop()

def curve_left_while_forward750():
    forward(0.25, 0.5)  # Move forward for 1 second at 50% speed
    left(0.50, 1) 
    forward(1, 0.5)   # 
    stop()

def curve_left_while_forward875():
    forward(0.25, 0.5)  # Move forward for 1 second at 50% speed
    left(0.35, 1) 
    forward(1, 0.5)   # 
    stop()

def curve_left_while_forward1000():
    forward(0.25, 0.5)  # Move forward for 1 second at 50% speed
    left(0.2, 1) 
    forward(1, 0.5)   # 
    stop()


curve_left_while_forward1000()