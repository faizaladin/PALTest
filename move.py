from gpiozero import Motor, PWMOutputDevice
import time
import cv2
import testcamera

ena = PWMOutputDevice(12)
enb = PWMOutputDevice(13)
motor_a = Motor(forward=17, backward=27)
motor_b = Motor(forward=5, backward=22)

def stop():
    motor_a.stop()
    motor_b.stop()

def grid_forward(en_value):
    ena.value = en_value
    enb.value = en_value
    motor_a.forward()
    motor_b.forward()

def forward(num, en_value):
    ena.value = en_value
    enb.value = en_value
    motor_a.forward()
    motor_b.forward()

def pos_right(num):
    ena.value = 0.87
    enb.value = 0.87
    motor_a.forward()
    motor_b.backward()
    time.sleep(num)

def backward(num):
    ena.value = 0.2
    enb.value = 0.2
    motor_a.backward()
    motor_b.backward()
    time.sleep(num)

def right(num, en_value):
    ena.value = en_value
    enb.value = en_value
    motor_a.forward()
    motor_b.backward()
    time.sleep(num)
    stop()

def left(num, en_value):
    ena.value = en_value
    enb.value = en_value
    motor_a.backward()
    motor_b.forward()
    time.sleep(num)
    stop()

def curve_left_while_forward125():
    ena_value = 0.25
    enb_value = 0.95
    ena.value = ena_value
    enb.value = enb_value
    motor_a.backward()
    motor_b.forward()
    time.sleep(2.2)
    grid_forward(0.2)
    time.sleep(1.2)
    stop()

def curve_left_while_forward250():
    forward(0.25, 0.2)  # Move forward for 1 second at 50% speed
    left(1.05, 0.87) 
    forward(4, 0.2)   # 

def curve_left_while_forward375():
    forward(0.25, 0.2)  # Move forward for 1 second at 50% speed
    left(0.95, 0.87) 
    forward(4, 0.2)   # 

def curve_left_while_forward500():
    forward(0.25, 0.2)  # Move forward for 1 second at 50% speed
    left(0.80, 0.87) 
    forward(4, 0.2)   # 

def curve_left_while_forward625():
    forward(0.25, 0.2)  # Move forward for 1 second at 50% speed
    left(0.65, 0.87) 
    forward(4, 0.2)   # 

def curve_left_while_forward750():
    forward(0.25, 0.2)  # Move forward for 1 second at 50% speed
    left(0.50, 0.87) 
    forward(4, 0.2)   # 

def curve_left_while_forward875():
    forward(0.25, 0.2)  # Move forward for 1 second at 50% speed
    left(0.35, 0.87) 
    forward(4, 0.2)   # 

def curve_left_while_forward1000():
    forward(0.25, 0.2)  # Move forward for 1 second at 50% speed
    left(0.2, 0.87) 
    forward(4, 0.2)   # 

def curve_right_while_forward125():
    forward(0.25, 0.5)  # Move forward for 1 second at 50% speed
    right(1.2, 0.87) 
    forward(4, 0.2)   # 

def curve_right_while_forward250():
    forward(0.25, 0.5)  # Move forward for 1 second at 50% speed
    right(1.05, 0.87) 
    forward(4, 0.2)   # 

def curve_right_while_forward375():
    forward(0.25, 0.5)  # Move forward for 1 second at 50% speed
    right(0.95, 0.87) 
    forward(4, 0.2)   # 

def curve_right_while_forward500():
    forward(0.25, 0.5)  # Move forward for 1 second at 50% speed
    right(0.80, 0.87) 
    forward(4, 0.2)   # 

def curve_right_while_forward625():
    forward(0.25, 0.2)  # Move forward for 1 second at 50% speed
    right(0.65, 0.87) 
    forward(4, 0.2)   # 

def curve_right_while_forward750():
    forward(0.25, 0.2)  # Move forward for 1 second at 50% speed
    right(0.50, 0.87) 
    forward(4, 0.2)   # 

def curve_right_while_forward875():
    forward(0.25, 0.2)  # Move forward for 1 second at 50% speed
    right(0.35, 0.87) 
    forward(4, 0.2)   # 

def curve_right_while_forward1000():
    forward(0.25, 0.2)  # Move forward for 1 second at 50% speed
    right(0.2, 0.87) 
    forward(4, 0.2)   # 

curve_left_while_forward125()
#forward(5, 0.2)