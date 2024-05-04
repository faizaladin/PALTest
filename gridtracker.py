import testcamera
import cv2
import time
import move

buffer_size = 20

# Initialize the camera
cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')  # Use 0 for the default camera

cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)

# Define the frame rate and the interval (in seconds) between captures

# Set the maximum number of images to capture
max_images = 5
image_count = 0

grids_hit = []

# List to store captured images
captured_images = []

move.grid_forward(0.2)

fps = cap.get(cv2.CAP_PROP_FPS)

currentFrame = 0

try:
    while image_count < max_images:
        # Capture frame-by-frame
        ret, frame = cap.read()
        captured_images.append([ret, frame])
        image_count += 1
        currentFrame += fps * 5
        cap.set(cv2.CAP_PROP_POS_FRAMES, currentFrame)
    move.stop()

finally:
    for i in range(len(captured_images)):
        # Display the image
        info = testcamera.calculate_orientation(captured_images[i][0], captured_images[i][1])
        print(info[0])
        grids_hit.append(testcamera.point_in_grid(info[0], info[2]))
        # Delay for a short time (adjust as needed)
        print(f"image {i} processed")
    print(grids_hit)