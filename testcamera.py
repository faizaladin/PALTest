import cv2
import numpy as np
import math

def detect_blue(image, region, rows, cols):
    x1, y1, x2, y2 = region  # Region coordinates (top-left and bottom-right)
    region_height, region_width = y2 - y1, x2 - x1
    
    row_step = region_height // rows
    col_step = region_width // cols

    deep_blue_coordinates = []

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

            # Define the lower and upper bounds for the deep blue color in HSV
            lower_deep_blue = np.array([90, 30, 10])  # Adjusted lower bound
            upper_deep_blue = np.array([130, 255, 120])

            # Threshold the HSV image to get only deep blue colors
            mask = cv2.inRange(hsv_roi, lower_deep_blue, upper_deep_blue)

            # Check if there are any deep blue pixels in the ROI
            if np.any(mask):
                # Find the coordinates of the deep blue pixel
                rows_deep_blue, cols_deep_blue = np.where(mask > 0)
                # Convert coordinates to be relative to the entire image
                deep_blue_x = cell_x1 + np.mean(cols_deep_blue)
                deep_blue_y = cell_y1 + np.mean(rows_deep_blue)
                deep_blue_coordinates.append((int(deep_blue_x), int(deep_blue_y)))

    return deep_blue_coordinates


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

grid_points = {}
# Function to draw a grid of squares within a specified region of an image
def draw_grid_within_region(image, region, rows, cols, radius=110):
    x1, y1, x2, y2 = region  # Region coordinates (top-left and bottom-right)
    region_height, region_width = y2 - y1, x2 - x1
    
    row_step = region_height // rows
    col_step = region_width // cols

    global grid_points  # Dictionary to store points within each grid square

    for i in range(rows):
        for j in range(cols):
            center_x = x1 + (j + 0.5) * col_step
            center_y = y1 + (i + 0.5) * row_step
            grid_number = i * cols + j + 1  # Calculate grid square number
            grid_points[grid_number] = set()  # Initialize empty set for points in this grid square
            # Find points around each center point
            for y in range(int(center_y - radius), int(center_y + radius + 1)):
                for x in range(int(center_x - radius), int(center_x + radius + 1)):
                    distance = np.linalg.norm(np.array((center_x, center_y)) - np.array((x, y)))
                    if distance <= radius:
                        # Normalize x-coordinate by subtracting 1250 and y-coordinate by subtracting from 1980
                        normalized_x = x - 1250
                        normalized_y = 1980 - y
                        grid_points[grid_number].add((normalized_x, normalized_y))

# Now grid_points is a dictionary where keys are grid coordinates and values are lists of points within each grid square


def find_center_of_robot(ret, img):

    # Define the region of the colony space (coordinates: top-left (x1, y1) and bottom-right (x2, y2))
    colony_region = (1250, 600, 2600, 1980)  # Example region coordinates

    # Capture video from the IP camera

    # Read a single frame

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
                #cv2.circle(rotated_img, (coord[1], coord[0]), 3, (0, 0, 255), -1)  # Red color
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
    # cap.release()
    # cv2.destroyAllWindows()

    return point_on_grid

def find_center_of_blue(robot_center, ret, img):

    points_to_keep = []

    # Define the region of the colony space (coordinates: top-left (x1, y1) and bottom-right (x2, y2))
    colony_region = (1250, 600, 2600, 1980)  # Example region coordinates
    
    buffer_size = 15

    # Capture video from the IP camera
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
                red_points.append(coord)  # Store red point coordinates
        # Apply blue filter
        lower_blue = np.array([100, 50, 50])  # Adjust this range for the specific color
        upper_blue = np.array([140, 255, 255]) # Adjusted upper bound
        mask_blue = cv2.inRange(cv2.cvtColor(rotated_img, cv2.COLOR_BGR2HSV), lower_blue, upper_blue)
        blue_filtered = cv2.bitwise_and(rotated_img, rotated_img, mask=mask_blue)

        # Find blue pixel coordinates from the filtered image
        blue_filter_coordinates = np.argwhere(mask_blue > 0)

        # Draw red points on the coordinates detected by the filter within the grid space
        for coord in blue_filter_coordinates:
            if colony_region[0] <= coord[1] <= colony_region[2] and colony_region[1] <= coord[0] <= colony_region[3]:
                red_points.append((coord[1], coord[0]))  # Store red point coordinates

        # Calculate distances of each red point from the robot center and store them with their respective points
        distances_with_points = [(math.sqrt((coord[0] - robot_center[0]) ** 2 + (coord[1] - robot_center[1]) ** 2), coord) for coord in red_points]

        # Sort the distances and points based on distances
        sorted_distances_with_points = sorted(distances_with_points)

        # Take only the closest 100 points with their distances
        closest_100_points_with_distances = sorted_distances_with_points[:1100]

        # Extract only the points from the sorted list of closest points with distances
        red_points = [point for (_, point) in closest_100_points_with_distances]

        # for coord in red_points:
        #     cv2.circle(rotated_img, coord, 3, (0, 0, 255), -1)  # Red color
        #print(red_points)

        # Calculate the average of red points
        if red_points:
            average_x = sum(pt[0] for pt in red_points) / len(red_points)
            average_y = sum(pt[1] for pt in red_points) / len(red_points)
            average_point = (int(average_x), int(average_y))
            point_on_grid = (int(average_x), int(average_y))

            robot_top = (robot_center[0], 600)

            # Draw a yellow dot at the average point
            cv2.circle(rotated_img, average_point, 5, (0, 255, 255), -1)  # Yellow color
            cv2.circle(rotated_img, robot_center, 5, (0, 255, 0), -1)
            cv2.circle(rotated_img, robot_top, 5, (0, 255, 0), -1)


        # Display the image with grid lines, detected blue, red points, blue filter, and yellow dot
        #cv2.imshow('Rotated Original with Grid, Detected Blue, Red Points, Blue Filter, and Yellow Dot', rotated_img)
        #cv2.waitKey(0)  # Wait for any key press to close the window

    # Release the video capture object and close all windows
    # cap.release()
    # cv2.destroyAllWindows()

    return point_on_grid

def slope(x1, y1, x2, y2): # Line slope given two points:
    if (x2-x1) == 0:
        return 10000000000
    return (y2-y1)/(x2-x1)

def angle(s1, s2): 
    return math.degrees(math.atan((s2-s1)/(1+(s2*s1))))

def normalize_angle(angle, quadrant_checker):
    if quadrant_checker[0] > 0 and quadrant_checker[1] > 0:
        return angle
    elif quadrant_checker[0] > 0 and quadrant_checker[1] < 0:
        return 180 - abs(angle)
    elif quadrant_checker[0] < 0 and quadrant_checker[1] < 0:
        return 180 + abs(angle)
    elif quadrant_checker[0] < 0 and quadrant_checker[1] > 0:
        return 360 - abs(angle)

    # Normalize the angle to be between 0 and 360 degrees
    normalized_angle = angle % 360
    return normalized_angle

def calculate_orientation(ret, img):
    # Assuming find_center_of_robot and find_center_of_blue functions are implemented
       # Assuming find_center_of_robot and find_center_of_blue functions are implemented
    robot_center = find_center_of_robot(ret, img)
    triangle_center = find_center_of_blue(robot_center, ret, img)

    adjusted_robot_center = (robot_center[0] - 1250, 1980 - robot_center[1])
    adjusted_triangle_center = (triangle_center[0]-1250, 1980 - triangle_center[1])

    robot_center = adjusted_robot_center
    triangle_center = adjusted_triangle_center

    quadrant_checker = ((triangle_center[0]-robot_center[0]), (triangle_center[1] - robot_center[1]))
    
    robot_top = (robot_center[0], 1380)

    slope1 = slope(robot_center[0], robot_center[1], triangle_center[0], triangle_center[1])
    slope2 = 10000000000

    initial_angle = angle(slope1, slope2)

    return [robot_center, normalize_angle(initial_angle, quadrant_checker), grid_points]

def point_in_grid(point, grid_points):
    for grid_num, points in grid_points.items():
        if point in points:
            return grid_num
    return None  # Return None if the point is not in any grid square
