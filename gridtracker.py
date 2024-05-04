import testcamera
import cv2
import time
import move

# Initialize the camera
cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')  # Use 0 for the default camera

# Define the frame rate and the interval (in seconds) between captures
frame_rate = 30  # Adjust this based on your camera capabilities
capture_interval = 1  # 1 second

# Set the maximum number of images to capture
max_images = 10
image_count = 0

# List to store captured images
captured_images = []

# Get the current time
start_time = time.time()
move.forward(1, 0.25)
try:
    while image_count < max_images:
        # Capture frame-by-frame
        ret, frame = cap.read()
        captured_images.append(frame)
    move.stop()

finally:
    print(len(captured_images))
