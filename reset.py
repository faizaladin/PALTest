from gpiozero import Motor, PWMOutputDevice
import time
import testcamera
import move 
import random

try:
    robot_info = testcamera.calculate_orientation()

    while robot_info[1] > 5 and robot_info[1] < 355:
        print(robot_info[1])
        if robot_info[1] < 5 or robot_info[1] > 355:
            break
        elif robot_info[1] > 90:
            move.right(random.uniform(0.15, 0.4), 0.85)
            move.stop()
        else:
            move.left(random.uniform(0.15, 0.4), 0.85)
            move.stop()
        time.sleep(2)
        print("checking")
        robot_info = testcamera.calculate_orientation()

    move.backward(6)
    move.forward(0.3, 0.25)
    print("working on turn")
    while robot_info[1] < 87 and robot_info[1] > 92:
        print(robot_info[1])
        if robot_info[1] > 87 or robot_info[1] <= 90:
            break
        elif robot_info[1] < 87:
            move.left(random.uniform(0.15, 0.4), 0.85)
            move.stop()
        else:
            move.right(random.uniform(0.15, 0.4), 0.85)
            move.stop()
        time.sleep(2)
        print("checking")
        robot_info = testcamera.calculate_orientation()

    move.backward(6)
    move.stop()

except KeyboardInterrupt:
    move.stop()