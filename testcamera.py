import cv2
import numpy as np

# Function to apply the green color filter
def filter_green(frame):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define range of green color in HSV
    lower_green = np.array([40, 40, 40])   # Adjust these values as needed
    upper_green = np.array([70, 255, 255])  # Adjust these values as needed
    
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    return res

# Capture video from the IP camera
cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')

while True:
    ret, img = cap.read()
    if not ret:
        break
    
    # Apply the green color filter
    green_filtered_img = filter_green(img)
    
    cv2.imshow('Original', img)
    cv2.imshow('Green Filter', green_filtered_img)
    
    k = cv2.waitKey(10) & 0xff
    if k == 27:  # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()