from gpiozero import Motor, PWMOutputDevice
import time
import testcamera
import move 
import random

robot_info = testcamera.calculate_orientation()

while robot_info[1] > 3 and robot_info[1] < 357:
    print(robot_info[1])
    if robot_info[1] < 3 or robot_info[1] > 357:
        break
    elif robot_info[1] > 90:
        move.right(random.uniform(0.2, 0.5), 1)
        move.stop()
    else:
        move.left(random.uniform(0.2, 0.5), 1)
        move.stop()
    time.sleep(2)
    print("checking")
    robot_info = testcamera.calculate_orientation()

print("done")
move.backward(6)
move.forward(0.3, 0.25)
move.right(1, 1)
move.backward(6)
move.stop()