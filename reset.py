from gpiozero import Motor, PWMOutputDevice
import time
import testcamera
import move 
import random
import cv2

def reset():

    buffer_size = 25

    # Initialize the camera
    cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')  # Use 0 for the default camera

    cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)

    move.curve_left_while_forward950()

    try:
        ret, frame = cap.read()
        robot_info = testcamera.calculate_orientation(ret, frame)

        while robot_info[1] > 5 and robot_info[1] < 355:
            #robot_info = testcamera.calculate_orientation(ret, frame)
            print(robot_info[1])
            if robot_info[1] < 5:
                print("less than 5")
                break
            if robot_info[1] > 355:
                print("more than 355")
                break
            if robot_info[1] <= 180:
                print("less than 180")
                move.left(random.uniform(0.15, 0.4), 0.87)
                move.stop()
            else:
                move.right(random.uniform(0.15, 0.4), 0.87)
                move.stop()
            time.sleep(2)
            print("checking")
            cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')  # Use 0 for the default camera
            cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
            ret, frame = cap.read()
            robot_info = testcamera.calculate_orientation(ret, frame)

        move.backward(5)
        move.stop()
        move.forward(0.7, 0.3)
        move.stop()
        # move.right(2, 0.87)
        # move.stop()
        # # print("working on turn")
        cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')  # Use 0 for the default camera
        cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
        ret, frame = cap.read()
        robot_info = testcamera.calculate_orientation(ret, frame)
        while robot_info[1] < 87 or robot_info[1] > 92:
            print(robot_info[1])
            if robot_info[1] > 91:
                move.left(random.uniform(0.15, 0.4), 0.87)
                move.stop()
            elif robot_info[1] < 87:
                move.right(random.uniform(0.15, 0.4), 0.87)
                move.stop()
            time.sleep(2)
            print("checking")
            cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')  # Use 0 for the default camera
            cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
            ret, frame = cap.read()
            robot_info = testcamera.calculate_orientation(ret, frame)
        move.backward(5)
        move.stop()

    except KeyboardInterrupt:
        move.stop()

reset()