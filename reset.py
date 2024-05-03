from gpiozero import Motor, PWMOutputDevice
import time
import testcamera
import move 
import random

while True:
    try:
        robot_info = testcamera.calculate_orientation()
        while robot_info[1] > 5 and robot_info[1] < 355:
            print(robot_info)
            if robot_info[1] > 90:
                move.right(random.uniform(0.1, 1), 1)
                move.stop()
            else:
                move.left(random.uniform(0.1, 1), 1)
                move.stop()
            time.sleep(2)
            print("checking")
            robot_info = testcamera.calculate_orientation()

    except KeyboardInterrupt:
        move.stop()

print(robot_info)