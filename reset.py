from gpiozero import Motor, PWMOutputDevice
import time
import testcamera
import move 

while true:
    try:
        robot_info = testcamera.calculate_orientation()
    while robot_info[1] > 2 and robot_info[1] < 358:
        print(robot_info)
        if robot_info[1] > 90:
            move.right(1/(robot_info[1]-90), 1)
            move.stop()
        else:
            move.left(1/(robot_info[1]-90), 1)
            move.stop()
        robot_info = testcamera.calculate_orientation()

    except KeyboardInterrupt:
        move.stop()
        GPIO.cleanup()

print(robot_info)