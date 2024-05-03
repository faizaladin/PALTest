import cv2
import numpy as np
import math

def detect_blue(image, region, rows, cols):
    x1, y1, x2, y2 = region  # Region coordinates (top-left and bottom-right)
    region_height, region_width = y2 - y1, x2 - x1
    
    row_step = region_height // rows
    col_step = region_width // cols

    blue_coordinates = []

    for i in range(rows):
        for j in range(cols):
            cell_x1 = x1 + j * col_step
            cell_y1 = y1 + i * row_step
            cell_x2 = x1 + (j + 1) * col_step
            cell_y2 = y1 + (i + 1) * row_step
            
            # Extract the region of interest (ROI) from the image
            roi = image[cell_y1:cell_y2, cell_x1:cell_x2]

            # Convert the ROI to HSV color space
            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # Define the lower and upper bounds for the blue color in HSV
            lower_blue = np.array([90, 50, 50])  # Adjusted lower bound
            upper_blue = np.array([130, 255, 255])  # Adjusted upper bound

            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv_roi, lower_blue, upper_blue)

            # Check if there are any blue pixels in the ROI
            if np.any(mask):
                # Find the coordinates of the blue pixel
                rows_blue, cols_blue = np.where(mask > 0)
                # Convert coordinates to be relative to the entire image
                blue_x = cell_x1 + np.mean(cols_blue)
                blue_y = cell_y1 + np.mean(rows_blue)
                blue_coordinates.append((int(blue_x), int(blue_y)))

    return blue_coordinates

# Function to detect lime green within the specified grid space and return its coordinates
def detect_lime_green(image, region, rows, cols):
    x1, y1, x2, y2 = region  # Region coordinates (top-left and bottom-right)
    region_height, region_width = y2 - y1, x2 - x1
    
    row_step = region_height // rows
    col_step = region_width // cols

    lime_green_coordinates = []

    for i in range(rows):
        for j in range(cols):
            cell_x1 = x1 + j * col_step
            cell_y1 = y1 + i * row_step
            cell_x2 = x1 + (j + 1) * col_step
            cell_y2 = y1 + (i + 1) * row_step
            
            # Extract the region of interest (ROI) from the image
            roi = image[cell_y1:cell_y2, cell_x1:cell_x2]

            # Convert the ROI to HSV color space
            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # Define the lower and upper bounds for the lime green color in HSV
            lower_lime_green = np.array([35, 50, 50])  # Adjusted lower bound
            upper_lime_green = np.array([90, 255, 255])  # Adjusted upper bound

            # Threshold the HSV image to get only lime green colors
            mask = cv2.inRange(hsv_roi, lower_lime_green, upper_lime_green)

            # Check if there are any lime green pixels in the ROI
            if np.any(mask):
                # Find the coordinates of the lime green pixel
                rows_green, cols_green = np.where(mask > 0)
                # Convert coordinates to be relative to the entire image
                green_x = cell_x1 + np.mean(cols_green)
                green_y = cell_y1 + np.mean(rows_green)
                lime_green_coordinates.append((int(green_x), int(green_y)))

    return lime_green_coordinates

# Function to draw a grid of squares within a specified region of an image
def draw_grid_within_region(image, region, rows, cols, color=(255, 255, 255), thickness=2):
    x1, y1, x2, y2 = region  # Region coordinates (top-left and bottom-right)
    region_height, region_width = y2 - y1, x2 - x1
    
    row_step = region_height // rows
    col_step = region_width // cols

    for i in range(rows + 1):  # Adjusted to draw grid lines on the boundary
        y = y1 + i * row_step
        cv2.line(image, (x1, y), (x2, y), color, thickness)
    for j in range(cols + 1):  # Adjusted to draw grid lines on the boundary
        x = x1 + j * col_step
        cv2.line(image, (x, y1), (x, y2), color, thickness)

    # Print the coordinates of the four corners of the grid
    # print("Top-left corner:", (x1, y1))
    # print("Top-right corner:", (x2, y1))
    # print("Bottom-left corner:", (x1, y2))
    # print("Bottom-right corner:", (x2, y2))

def find_center_of_robot():

    # Define the region of the colony space (coordinates: top-left (x1, y1) and bottom-right (x2, y2))
    colony_region = (1250, 600, 2600, 1980)  # Example region coordinates

    # Capture video from the IP camera
    cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')

    # Read a single frame
    ret, img = cap.read()

    # If the frame is successfully read
    if ret:
        # Rotate the entire image
        angle = -15  # Rotation angle in degrees
        center = ((colony_region[0] + colony_region[2]) // 2, (colony_region[1] + colony_region[3]) // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
        rotated_img = cv2.warpAffine(img, rotation_matrix, (img.shape[1], img.shape[0]))

        # Draw grid lines within the colony space region and print corner coordinates
        draw_grid_within_region(rotated_img, colony_region, 5, 5)  # Adjust the number of rows and columns as needed

        # Detect lime green within the grid space
        lime_green_coordinates = detect_lime_green(rotated_img, colony_region, 5, 5)

        # Draw red points on all lime green coordinates within the grid space
        red_points = []  # Array to store red point coordinates
        for coord in lime_green_coordinates:
            if colony_region[0] <= coord[0] <= colony_region[2] and colony_region[1] <= coord[1] <= colony_region[3]:
                cv2.circle(rotated_img, coord, 3, (0, 0, 255), -1)  # Red color
                red_points.append(coord)  # Store red point coordinates

        # Apply lime green filter
        lower_lime_green = np.array([35, 50, 50])  # Adjusted lower bound
        upper_lime_green = np.array([90, 255, 255])  # Adjusted upper bound
        mask_lime_green = cv2.inRange(cv2.cvtColor(rotated_img, cv2.COLOR_BGR2HSV), lower_lime_green, upper_lime_green)
        lime_green_filtered = cv2.bitwise_and(rotated_img, rotated_img, mask=mask_lime_green)

        # Find lime green pixel coordinates from the filtered image
        lime_green_filter_coordinates = np.argwhere(mask_lime_green > 0)

        # Draw red points on the coordinates detected by the filter within the grid space
        for coord in lime_green_filter_coordinates:
            if colony_region[0] <= coord[1] <= colony_region[2] and colony_region[1] <= coord[0] <= colony_region[3]:
                cv2.circle(rotated_img, (coord[1], coord[0]), 3, (0, 0, 255), -1)  # Red color
                red_points.append((coord[1], coord[0]))  # Store red point coordinates

        # Calculate the average of red points
        if red_points:
            average_x = sum(pt[0] for pt in red_points) / len(red_points)
            average_y = sum(pt[1] for pt in red_points) / len(red_points)
            average_point = (int(average_x), int(average_y))
            point_on_grid = (int(average_x), int(average_y))

            # Draw a blue dot at the average point
            cv2.circle(rotated_img, average_point, 5, (255, 0, 0), -1)  # Blue color

        # Display the image with grid lines, detected lime green, red points, lime green filter, and blue dot
        #cv2.imshow('Rotated Original with Grid, Detected Lime Green, Red Points, Lime Green Filter, and Blue Dot', rotated_img)
        #cv2.waitKey(0)  # Wait for any key press to close the window

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

    return point_on_grid

def find_center_of_blue():

    # Define the region of the colony space (coordinates: top-left (x1, y1) and bottom-right (x2, y2))
    colony_region = (1250, 600, 2600, 1980)  # Example region coordinates

    # Capture video from the IP camera
    cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')

    # Read a single frame
    ret, img = cap.read()

    # If the frame is successfully read
    if ret:
        # Rotate the entire image
        angle = -15  # Rotation angle in degrees
        center = ((colony_region[0] + colony_region[2]) // 2, (colony_region[1] + colony_region[3]) // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
        rotated_img = cv2.warpAffine(img, rotation_matrix, (img.shape[1], img.shape[0]))

        # Draw grid lines within the colony space region and print corner coordinates
        draw_grid_within_region(rotated_img, colony_region, 5, 5)  # Adjust the number of rows and columns as needed

        # Detect blue within the grid space
        blue_coordinates = detect_blue(rotated_img, colony_region, 5, 5)

        # Draw red points on all blue coordinates within the grid space
        red_points = []  # Array to store red point coordinates
        for coord in blue_coordinates:
            if colony_region[0] <= coord[0] <= colony_region[2] and colony_region[1] <= coord[1] <= colony_region[3]:
                cv2.circle(rotated_img, coord, 3, (0, 0, 255), -1)  # Red color
                red_points.append(coord)  # Store red point coordinates

        # Apply blue filter
        lower_blue = np.array([90, 50, 50])  # Adjusted lower bound
        upper_blue = np.array([130, 255, 255])  # Adjusted upper bound
        mask_blue = cv2.inRange(cv2.cvtColor(rotated_img, cv2.COLOR_BGR2HSV), lower_blue, upper_blue)
        blue_filtered = cv2.bitwise_and(rotated_img, rotated_img, mask=mask_blue)

        # Find blue pixel coordinates from the filtered image
        blue_filter_coordinates = np.argwhere(mask_blue > 0)

        # Draw red points on the coordinates detected by the filter within the grid space
        for coord in blue_filter_coordinates:
            if colony_region[0] <= coord[1] <= colony_region[2] and colony_region[1] <= coord[0] <= colony_region[3]:
                cv2.circle(rotated_img, (coord[1], coord[0]), 3, (0, 0, 255), -1)  # Red color
                red_points.append((coord[1], coord[0]))  # Store red point coordinates

        # Calculate the average of red points
        if red_points:
            average_x = sum(pt[0] for pt in red_points) / len(red_points)
            average_y = sum(pt[1] for pt in red_points) / len(red_points)
            average_point = (int(average_x), int(average_y))
            point_on_grid = (int(average_x), int(average_y))

            # Draw a yellow dot at the average point
            cv2.circle(rotated_img, average_point, 5, (0, 255, 255), -1)  # Yellow color

        # Display the image with grid lines, detected blue, red points, blue filter, and yellow dot
        #cv2.imshow('Rotated Original with Grid, Detected Blue, Red Points, Blue Filter, and Yellow Dot', rotated_img)
        #cv2.waitKey(0)  # Wait for any key press to close the window

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

    return point_on_grid

def calculate_orientation():
    robot_center = find_center_of_robot()
    triangle_center = find_center_of_blue()
    # Coordinates of corners
    top_left_corner = (1250, 600)
    bottom_left_corner = (0, 0)
    top_right = (2600, 600)
    bottom_right = (1350, 0)

    # Adjust coordinates
    robot_center = (robot_center[0] - 1250, 1980 - robot_center[1])
    triangle_center = (triangle_center[0] - 1250, 1980 - triangle_center[1])

    # Calculate vectors
    vec1 = (top_left_corner[0] - robot_center[0], top_left_corner[1] - robot_center[1])
    vec2 = (triangle_center[0] - robot_center[0], triangle_center[1] - robot_center[1])

    # Calculate angle between vectors
    angle_rad = math.atan2(vec2[1], vec2[0]) - math.atan2(vec1[1], vec1[0])
    angle_deg = math.degrees(angle_rad)

    # Convert angle to the range (0, 360) with top as 0, right as 90, bottom as 180, and left as 270
    angle_deg = (90 - angle_deg) % 360

    return [robot_center, angle_deg]

info = calculate_orientation()
print(info)