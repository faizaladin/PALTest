import tkinter as tk
import random
import time

grid_points = {}  # Define grid_points as a global variable
grid_size = 5
cell_size = 80
robot_position = (4, 0)
robot_orientation = "right"  # Initial orientation

def generate_grid_points(grid_size=5, cell_size=80):
    global grid_points  # Use the global grid_points variable
    count = 1
    for i in range(grid_size):
        for j in range(grid_size):
            x0, y0 = j * cell_size, i * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            points = set((x, y) for x in range(x0, x1) for y in range(y0, y1))
            grid_points[count] = points
            count += 1

def draw_grid(canvas):
    global robot_position
    global robot_orientation
    count = 1
    global grid_size
    global cell_size
    for i in range(grid_size):
        for j in range(grid_size):
            x0, y0 = j * cell_size, i * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
            x_center = (x0 + x1) / 2
            y_center = (y0 + y1) / 2
            canvas.create_text(x_center, y_center, text=str(count), fill="red")
            count += 1
            if (i, j) == robot_position:
                # Calculate the center of the robot in terms of pixels
                canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="blue")
                # Draw orientation arrow based on the robot's orientation
                if robot_orientation == "up":
                    canvas.create_line(x_center, y_center, x_center, y_center - 20, fill="black", width=2)
                elif robot_orientation == "down":
                    canvas.create_line(x_center, y_center, x_center, y_center + 20, fill="black", width=2)
                elif robot_orientation == "left":
                    canvas.create_line(x_center, y_center, x_center - 20, y_center, fill="black", width=2)
                elif robot_orientation == "right":
                    canvas.create_line(x_center, y_center, x_center + 20, y_center, fill="black", width=2)

def find_robot_position(robot_coordinates):
    for i in range(grid_size):
        for j in range(grid_size):
            x0, y0 = j * cell_size, i * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            x_center = (x0 + x1) / 2
            y_center = (y0 + y1) / 2
            if (i, j) == robot_coordinates:
                # Calculate the center of the robot in terms of pixels
                robot_pixel_x = x_center
                robot_pixel_y = y_center
    return robot_pixel_x, robot_pixel_y  # Return the pixel coordinates of the robot

def find_robot_grid(robot_position, grid_points):
    for key, points in grid_points.items():
        if robot_position in points:
            return key
    return None  # Return None if the robot is not in any grid square

def forward(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if robot_orientation == "up":
            robot_position = (robot_position[0] - 1, robot_position[1])
        elif robot_orientation == "down":
            robot_position = (robot_position[0] + 1, robot_position[1])
        elif robot_orientation == "left":
            robot_position = (robot_position[0], robot_position[1] - 1)
        elif robot_orientation == "right":
            robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_left_forward125(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 0:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1] - 1)
                robot_orientation = "left"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1] + 1)
                robot_orientation = "right"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] + 1, robot_position[1] - 1)
                robot_orientation = "down"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] - 1, robot_position[1] + 1)
                robot_orientation = "up"
        else:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_left_forward250(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 1:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1] - 1)
                robot_orientation = "left"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1] + 1)
                robot_orientation = "right"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] + 1, robot_position[1] - 1)
                robot_orientation = "down"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] - 1, robot_position[1] + 1)
                robot_orientation = "up"
        elif i != 4:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_left_forward375(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 2:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
                robot_orientation = "left"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
                robot_orientation = "right"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] + 1, robot_position[1])
                robot_orientation = "down"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] - 1, robot_position[1])
                robot_orientation = "up"
        elif i !=4:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_left_forward500(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 2:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1] - 1)
                robot_orientation = "left"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1] + 1)
                robot_orientation = "right"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] + 1, robot_position[1] - 1)
                robot_orientation = "down"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] - 1, robot_position[1] + 1)
                robot_orientation = "up"
        elif i != 4:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_left_forward625(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 3:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
                robot_orientation = "left"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
                robot_orientation = "right"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] + 1, robot_position[1])
                robot_orientation = "down"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] - 1, robot_position[1])
                robot_orientation = "up"
        elif i !=4:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_left_forward750(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 3:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1] - 1)
                robot_orientation = "left"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1] + 1)
                robot_orientation = "right"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] + 1, robot_position[1] - 1)
                robot_orientation = "down"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] - 1, robot_position[1] + 1)
                robot_orientation = "up"
        elif i != 4:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_left_forward875(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 4:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
                robot_orientation = "left"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
                robot_orientation = "right"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] + 1, robot_position[1])
                robot_orientation = "down"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] - 1, robot_position[1])
                robot_orientation = "up"
        else:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_right_forward125(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 0:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1] + 1)
                robot_orientation = "right"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1] - 1)
                robot_orientation = "left"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] - 1, robot_position[1] - 1)
                robot_orientation = "up"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] + 1, robot_position[1] + 1)
                robot_orientation = "down"
        else:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_right_forward250(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 1:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1] + 1)
                robot_orientation = "right"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1] - 1)
                robot_orientation = "left"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] - 1, robot_position[1] - 1)
                robot_orientation = "up"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] + 1, robot_position[1] + 1)
                robot_orientation = "down"
        elif i != 4:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_right_forward375(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 2:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
                robot_orientation = "right"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
                robot_orientation = "left"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] - 1, robot_position[1])
                robot_orientation = "up"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] + 1, robot_position[1])
                robot_orientation = "down"
        elif i != 4:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_right_forward500(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 2:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1] + 1)
                robot_orientation = "right"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1] - 1)
                robot_orientation = "left"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] - 1, robot_position[1] - 1)
                robot_orientation = "up"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] + 1, robot_position[1] + 1)
                robot_orientation = "down"
        elif i != 4:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_right_forward625(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 3:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1] + 1)
                robot_orientation = "right"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1] - 1)
                robot_orientation = "left"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] - 1, robot_position[1] - 1)
                robot_orientation = "up"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] + 1, robot_position[1] + 1)
                robot_orientation = "down"
        elif i != 4:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_right_forward750(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 3:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1] + 1)
                robot_orientation = "right"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1] - 1)
                robot_orientation = "left"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] - 1, robot_position[1] - 1)
                robot_orientation = "up"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] + 1, robot_position[1] + 1)
                robot_orientation = "down"
        elif i != 4:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit

def curve_right_forward875(canvas):
    global robot_position
    global robot_orientation
    grids_hit = []  # Decide how many steps to move forward
    for i in range(5):
        draw_grid(canvas)
        robot_pixel_x, robot_pixel_y = find_robot_position(robot_position)
        grids_hit.append(find_robot_grid((robot_pixel_x, robot_pixel_y), grid_points))
        if i == 4:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1] + 1)
                robot_orientation = "right"
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1] - 1)
                robot_orientation = "left"
            elif robot_orientation == "left":
                robot_position = (robot_position[0] - 1, robot_position[1] - 1)
                robot_orientation = "up"
            elif robot_orientation == "right":
                robot_position = (robot_position[0] + 1, robot_position[1] + 1)
                robot_orientation = "down"
        else:
            if robot_orientation == "up":
                robot_position = (robot_position[0] - 1, robot_position[1])
            elif robot_orientation == "down":
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_orientation == "left":
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_orientation == "right":
                robot_position = (robot_position[0], robot_position[1] + 1)
        # Check if robot hits the boundary and adjust its position
        if robot_position[0] < 0:
            robot_position = (0, robot_position[1])
        elif robot_position[0] >= grid_size:
            robot_position = (grid_size - 1, robot_position[1])
        if robot_position[1] < 0:
            robot_position = (robot_position[0], 0)
        elif robot_position[1] >= grid_size:
            robot_position = (robot_position[0], grid_size - 1)
    return grids_hit


def turn_left():
    global robot_orientation
    if robot_orientation == "up":
        robot_orientation = "left"
    elif robot_orientation == "down":
        robot_orientation = "right"
    elif robot_orientation == "left":
        robot_orientation = "down"
    elif robot_orientation == "right":
        robot_orientation = "up"

def turn_right():
    global robot_orientation
    if robot_orientation == "up":
        robot_orientation = "right"
    elif robot_orientation == "down":
        robot_orientation = "left"
    elif robot_orientation == "left":
        robot_orientation = "up"
    elif robot_orientation == "right":
        robot_orientation = "down"

def start_simulation(direction_of_movement1, amount_of_curve1, direction_of_turn1, amount_of_turn1, direction_of_movement2, amount_of_curve2, direction_of_turn2, amount_of_turn2, number_of_loops):
    global robot_position
    global robot_orientation
    grids_hit = []
    grids_hit.append(21)
    root = tk.Tk()
    i = 1
    generate_grid_points(grid_size, cell_size)
    canvas = tk.Canvas(root, width=grid_size*cell_size, height=grid_size*cell_size)
    canvas.pack()

    direction_of_movement = direction_of_movement1
    amount_of_curve = amount_of_curve1
    direction_of_turn = direction_of_turn1
    amount_of_turn = amount_of_turn1

    while i < number_of_loops*2:
        # print(f"direction of movement: {direction_of_movement}")
        # print(f"amount of curve: {amount_of_curve}")
        #direction_of_movement = 0
        if int(direction_of_movement) == 0:
            if amount_of_curve == 0:
                grids_hit.extend(forward(canvas))
            if amount_of_curve == 1:
                grids_hit.extend(curve_right_forward125(canvas))
            if amount_of_curve == 2:
                grids_hit.extend(curve_right_forward250(canvas))
            if amount_of_curve == 3:
                grids_hit.extend(curve_right_forward375(canvas))
            if amount_of_curve == 4:
                grids_hit.extend(curve_right_forward500(canvas))
            if amount_of_curve == 5:
                grids_hit.extend(curve_right_forward625(canvas))
            if amount_of_curve == 6:
                grids_hit.extend(curve_right_forward750(canvas))
            if amount_of_curve == 7:
                grids_hit.extend(curve_right_forward875(canvas))
            #all left movement
        if int(direction_of_movement) == 1:
            if amount_of_curve == 0:
                grids_hit.extend(forward(canvas))
            if amount_of_curve == 1:
                grids_hit.extend(curve_left_forward125(canvas))
            if amount_of_curve == 2:
                grids_hit.extend(curve_left_forward250(canvas))
            if amount_of_curve == 3:
                grids_hit.extend(curve_left_forward375(canvas))
            if amount_of_curve == 4:
                grids_hit.extend(curve_left_forward500(canvas))
            if amount_of_curve == 5:
                grids_hit.extend(curve_left_forward625(canvas))
            if amount_of_curve == 6:
                grids_hit.extend(curve_left_forward750(canvas))
            if amount_of_curve == 7:
                grids_hit.extend(curve_left_forward875(canvas))
            
        if int(direction_of_turn) == 0:
            for x in range(int(amount_of_turn)):
                #print("turning right")
                turn_right()
        if int(direction_of_turn) == 1:
            for z in range(int(amount_of_turn)):
                #print("turning left")
                turn_left()

        if i % 2 == 0:
            direction_of_movement = direction_of_movement1
            amount_of_curve = amount_of_curve1
            direction_of_turn = direction_of_turn1
            amount_of_turn = amount_of_turn1
        if i % 2 != 0:
            direction_of_movement = direction_of_movement2
            amount_of_curve = amount_of_curve2
            direction_of_turn = direction_of_turn2
            amount_of_turn = amount_of_turn2

        i += 1
        
    
    # grids_hit.extend(curve_left_forward875(canvas))
    draw_grid(canvas)

    # print(grids_hit)
    # print(robot_position)
    root.mainloop()

    return grids_hit

def fitness_function(individual):
    direction_of_movement_1 = individual[0]  # Bit 0: 0 - right, 1 - left
    amount_of_curve_1 = int("".join(map(str, individual[1:4])), 2)  # Bits 1-3: Amount of curve for movement
    direction_of_turn_1 = individual[4]  # Bit 4: 0 - right, 1 - left
    amount_of_turn_1 = int("".join(map(str, individual[5:7])), 2)  # Bits 5-6: Amount of turn
    direction_of_movement_2 = individual[7]  # Bit 7: 0 - right, 1 - left
    amount_of_curve_2 = int("".join(map(str, individual[8:11])), 2)  # Bits 8-10: Amount of curve for movement
    direction_of_turn_2 = individual[11]  # Bit 11: 0 - right, 1 - left
    amount_of_turn_2 = int("".join(map(str, individual[12:14])), 2)  # Bits 12-13: Amount of turn
    number_of_loops = int("".join(map(str, individual[14:17])), 2)  # Bits 14-16: Number of times to loop through

    grids_hit = start_simulation(direction_of_movement_1, amount_of_curve_1, direction_of_turn_1, amount_of_turn_1, direction_of_movement_2, amount_of_curve_2, direction_of_turn_2, amount_of_turn_2, number_of_loops)
    print(grids_hit)
    return grids_hit

fitness_function('11111010111001011')
# Example usage
# start_simulation()
