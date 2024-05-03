from gpiozero import Motor, PWMOutputDevice
import time
import testcamera
import move 
import random

robot_info = testcamera.calculate_orientation()

while robot_info[1] > 5 and robot_info[1] < 355:
    print(robot_info[1])
    if robot_info[1] < 2 or robot_info[1] > 358:
        break
    elif robot_info[1] > 90:
        move.right(random.uniform(0.1, 0.5), 0.87)
        move.stop()
    else:
        move.left(random.uniform(0.1, 0.5), 0.87)
        move.stop()
    time.sleep(2)
    print("checking")
    robot_info = testcamera.calculate_orientation()

print("done")
move.backward(6)