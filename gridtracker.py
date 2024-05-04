import testcamera
import cv2
import time
import move

buffer_size = 15

# Initialize the camera
cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')  # Use 0 for the default camera

cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)

# Define the frame rate and the interval (in seconds) between captures

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
        image_count += 1
    move.stop()

finally:
    for i in range(len(captured_images)):
        cv.imshow(captured_images[i])
    print(len(captured_images))