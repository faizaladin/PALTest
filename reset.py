import testcamera
import move 

robot_info = testcamera.calculate_orientation()

while robot_info[1] > 2 or robot_info[1] < 358:
    if robot_info[2] > 90:
        move.right(0.5)
    else:
        move.left(0.5)
    robot_info = testcamera.calculate_orientation()

print(robot_info)