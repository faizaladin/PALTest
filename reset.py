from gpiozero import Motor, PWMOutputDevice
import time
import testcamera
import move 
import random

buffer_size = 20

# Initialize the camera
cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')  # Use 0 for the default camera

cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)

try:
    ret, frame = cap.read()
    robot_info = testcamera.calculate_orientation(ret, frame)

    while robot_info[1] > 5 and robot_info[1] < 355:
        robot_info = testcamera.calculate_orientation(ret, frame)
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
        cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')  # Use 0 for the default camera
        cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
        ret, frame = cap.read()
        robot_info = testcamera.calculate_orientation(ret, frame)

    move.backward(6)
    move.forward(0.3, 0.25)
    move.stop()
    print("working on turn")
    cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')  # Use 0 for the default camera
    cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
    ret, frame = cap.read()
    robot_info = testcamera.calculate_orientation(ret, frame)
    while robot_info[1] < 90 or robot_info[1] > 91.5:
        print(robot_info[1])
        if robot_info[1] > 91.5:
            move.left(random.uniform(0.15, 0.4), 0.85)
            move.stop()
        elif robot_info[1] < 90:
            move.right(random.uniform(0.15, 0.4), 0.85)
            move.stop()
        time.sleep(2)
        print("checking")
        cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')  # Use 0 for the default camera
        cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
        ret, frame = cap.read()
        robot_info = testcamera.calculate_orientation(ret, frame)
    move.backward(6)
    move.stop()

except KeyboardInterrupt:
    move.stop()