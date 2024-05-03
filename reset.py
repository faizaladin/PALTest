from gpiozero import Motor, PWMOutputDevice
import time
import testcamera
import move 
import random

while True:
    try:
        robot_info = testcamera.calculate_orientation()
        while robot_info[1] > 5 and robot_info[1] < 355:
            print(robot_info[1])
            if robot_info[1] < 5 or robot_info[1] > 355:
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
    except KeyboardInterrupt:
        move.stop()
        close_all()
