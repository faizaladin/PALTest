import cv2
import numpy as np

# Read the image
cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')

    # Read a single frame
ret, image = cap.read()

# Convert BGR to HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the lower and upper bounds for deep blue
lower_bound = np.array([100, 50, 50])  # Adjust this range for the specific color
upper_bound = np.array([140, 255, 255])

# Create a mask based on the color range
mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

# Apply the mask to the original image
filtered_image = cv2.bitwise_and(image, image, mask=mask)

# Display the original image and the filtered image
cv2.imshow('Original Image', image)
cv2.imshow('Filtered Image', filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
