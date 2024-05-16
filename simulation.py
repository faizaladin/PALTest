import tkinter as tk
import random
import time
import math

grid_points = {}  # Define grid_points as a global variable
grid_size = 5
cell_size = 80
robot_position = (30, 370, 30)
#robot_position = (370, 370, 30)
robot_orientation = 90 # Initial orientation
#robot_orientation = 270
edge_point = (0,0)
min_x = 0
max_x = grid_size * cell_size
min_y = 0
max_y = grid_size * cell_size

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
            create_circle(robot_position[0], robot_position[1], robot_position[2], robot_orientation, canvas)
            
def find_robot_grid(robot_position, grid_points):
    grids = []
    for key, points in grid_points.items():
        if (robot_position[0], robot_position[1]) in points:
            return key
    return None  # Return None if the robot is not in any grid square

def create_circle(x, y, r, robot_orientation, canvas): #center coordinates, radius
    global edge_point
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    canvas.create_oval(x0, y0, x1, y1, fill="black")
    length_of_line = r  # Line length equal to circle radius
    end_x = x + length_of_line * math.sin(math.radians(robot_orientation))
    end_y = y - length_of_line * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
    edge_point = (end_x, end_y)
    # Draw the line
    canvas.create_line(x, y, end_x, end_y, fill="blue", width=2)

def forward(canvas, distance):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    step = 20
    curr_step = 0
    while curr_step < distance:
        #print(robot_position)
        robot_position = (int(robot_position[0]), int(robot_position[1]), robot_position[2])
        grids_hit.append(find_robot_grid(robot_position, grid_points))
        #print(edge_point)
        # Calculate the movement components
        delta_x = step * math.sin(math.radians(robot_orientation))  # Switched sin and cos
        delta_y = -step * math.cos(math.radians(robot_orientation))  # Switched sin and cos

        # Update the robot's position
        robot_position = (robot_position[0] + delta_x, robot_position[1] + delta_y, robot_position[2])
        edge_point = (edge_point[0] + delta_x, edge_point[1] + delta_y)
        if (edge_point[0] > max_x):
            robot_position = (max_x - robot_position[2], robot_position[1], robot_position[2])
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            return grids_hit
        if (edge_point[0] < 0):
            robot_position = (robot_position[2], robot_position[1], robot_position[2])
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            return grids_hit
        if (edge_point[1] < 0):
            robot_position = (robot_position[0], robot_position[2], robot_position[2])
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            return grids_hit
        if (edge_point[1] > max_y):
            robot_position = (robot_position[0], max_y - (robot_position[1]-max_y), robot_position[2])
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            return grids_hit
        # Redraw the grid with the new position
        # canvas.delete("all")  # Clear the canvas
        # draw_grid(canvas)
        
        # Update the current step
        curr_step += step
        
        # Update the canvas to visualize each step
        # canvas.update()
        # time.sleep(0.1)  # Adjust the sleep duration as needed
    return grids_hit

def curve_left_forward125(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation - 90
    if robot_orientation < 90:
        normalized_point = 360 + forward_point
        while robot_orientation > 0:
            robot_orientation -= 17
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 360
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation > normalized_point:
            robot_orientation -= 17
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation > forward_point:
            robot_orientation -= 17
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    grids_hit.extend(forward(canvas, 210))
    return grids_hit

def curve_left_forward250(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation - 90
    if robot_orientation < 90:
        normalized_point = 360 + forward_point
        while robot_orientation > 0:
            robot_orientation -= 11
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 360
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation > normalized_point:
            robot_orientation -= 11
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation > forward_point:
            robot_orientation -= 11
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    grids_hit.extend(forward(canvas, 110))
    return grids_hit

def curve_left_forward375(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation - 90
    grids_hit.extend(forward(canvas, 60))
    if robot_orientation < 90:
        normalized_point = 360 + forward_point
        while robot_orientation > 0:
            robot_orientation -= 12
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 360
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation > normalized_point:
            robot_orientation -= 12
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation > forward_point:
            robot_orientation -= 12
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    grids_hit.extend(forward(canvas, 110))
    return grids_hit

def curve_left_forward500(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation - 90
    grids_hit.extend(forward(canvas, 70))
    if robot_orientation < 90:
        normalized_point = 360 + forward_point
        while robot_orientation > 0:
            robot_orientation -= 11
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 360
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation > normalized_point:
            robot_orientation -= 11
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation > forward_point:
            robot_orientation -= 11
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    grids_hit.extend(forward(canvas, 30))
    return grids_hit

def curve_left_forward625(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation - 90
    grids_hit.extend(forward(canvas, 140))
    if robot_orientation < 90:
        normalized_point = 360 + forward_point
        while robot_orientation > 0:
            robot_orientation -= 12
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 360
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation > normalized_point:
            robot_orientation -= 12
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation > forward_point:
            robot_orientation -= 12
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    grids_hit.extend(forward(canvas, 40))
    return grids_hit

def curve_left_forward750(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation - 90
    grids_hit.extend(forward(canvas, 170))
    if robot_orientation < 90:
        normalized_point = 360 + forward_point
        while robot_orientation > 0:
            robot_orientation -= 15
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 360
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation > normalized_point:
            robot_orientation -= 15
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation > forward_point:
            robot_orientation -= 15
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    #grids_hit.extend(forward(canvas, 10))
    return grids_hit

def curve_left_forward875(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation - 90
    grids_hit.extend(forward(canvas, 250))
    #print(robot_position)
    if robot_orientation < 90:
        normalized_point = 360 + forward_point
        while robot_orientation > 0:
            robot_orientation -= 15
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 360
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation > normalized_point:
            robot_orientation -= 15
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation > forward_point:
            robot_orientation -= 15
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    #grids_hit.extend(forward(canvas, 10))
    #print(robot_position)
    return grids_hit

def curve_1000(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    return forward(canvas, 330)

def curve_right_forward125(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation + 90
    if robot_orientation > 270:
        normalized_point = forward_point - 360
        while robot_orientation < 360:
            robot_orientation += 17
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 0
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation < normalized_point:
            robot_orientation += 17
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation < 360:
            robot_orientation += 17
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    grids_hit.extend(forward(canvas, 210))
    return grids_hit

def curve_right_forward250(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation + 90
    if robot_orientation > 270:
        normalized_point = forward_point - 360
        while robot_orientation < 360:
            robot_orientation += 11
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 0
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation < normalized_point:
            robot_orientation += 11
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation < 360:
            robot_orientation += 11
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    grids_hit.extend(forward(canvas, 110))
    return grids_hit

def curve_right_forward375(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation + 90
    grids_hit.extend(forward(canvas, 60))
    if robot_orientation > 270:
        normalized_point = forward_point - 360
        while robot_orientation < 360:
            robot_orientation += 12
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 0
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation < normalized_point:
            robot_orientation += 12
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation < 360:
            robot_orientation += 12
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    grids_hit.extend(forward(canvas, 110))
    return grids_hit

def curve_right_forward500(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation + 90
    grids_hit.extend(forward(canvas, 70))
    if robot_orientation > 270:
        normalized_point = forward_point - 360
        while robot_orientation < 360:
            robot_orientation += 11
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 0
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation < normalized_point:
            robot_orientation += 11
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation < 360:
            robot_orientation += 11
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    grids_hit.extend(forward(canvas, 30))
    return grids_hit

def curve_right_forward625(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation + 90
    grids_hit.extend(forward(canvas, 140))
    if robot_orientation > 270:
        normalized_point = forward_point - 360
        while robot_orientation < 360:
            robot_orientation += 12
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 0
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation < normalized_point:
            robot_orientation += 12
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation < 360:
            robot_orientation += 12
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    grids_hit.extend(forward(canvas, 40))
    return grids_hit

def curve_right_forward750(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation + 90
    grids_hit.extend(forward(canvas, 170))
    if robot_orientation > 270:
        normalized_point = forward_point - 360
        while robot_orientation < 360:
            robot_orientation += 15
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 0
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation < normalized_point:
            robot_orientation += 15
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation < 360:
            robot_orientation += 15
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    #grids_hit.extend(forward(canvas, 40))
    return grids_hit

def curve_right_forward875(canvas):
    grids_hit = []
    global grid_points
    global robot_position
    global robot_orientation
    global edge_point
    global max_x
    global max_y
    forward_point = robot_orientation + 90
    grids_hit.extend(forward(canvas, 250))
    if robot_orientation > 270:
        normalized_point = forward_point - 360
        while robot_orientation < 360:
            robot_orientation += 15
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = 0
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
        while robot_orientation < normalized_point:
            robot_orientation += 15
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = normalized_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    else:
        while robot_orientation < 360:
            robot_orientation += 15
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            grids_hit.extend(forward(canvas, 20))
            # canvas.delete("all")  # Clear the canvas
            # draw_grid(canvas)
            # canvas.update()
            # time.sleep(0.1)  # Adjus
        robot_orientation = forward_point
        end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
        end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
        edge_point = (end_x, end_y)
    #grids_hit.extend(forward(canvas, 40))
    return grids_hit

def turn_left(num):
    global robot_position
    global robot_orientation
    global edge_point
    if num == 1:
        if robot_orientation < 30:
            robot_orientation = 360 - (30 - robot_orientation)
        else:
            robot_orientation -= 30
    if num == 2:
        if robot_orientation < 60:
            robot_orientation = 360 - (60 - robot_orientation)
        else:
            robot_orientation -= 60
    if num == 3:
        if robot_orientation < 90:
            robot_orientation = 360 - (90 - robot_orientation)
        else:
            robot_orientation -= 90
    
    end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
    end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
    edge_point = (end_x, end_y)

def turn_right(num):
    global robot_position
    global robot_orientation
    global edge_point
    if robot_orientation == 360:
        robot_orientation = 0
    if num == 1:
        if robot_orientation > 330:
            robot_orientation = (360 - robot_orientation)
        else:
            robot_orientation += 30
    if num == 2:
        if robot_orientation > 300:
            robot_orientation = (360 - robot_orientation)
        else:
            robot_orientation += 60
    if num == 3:
        if robot_orientation > 270:
            robot_orientation = 360 - robot_orientation
        else:
            robot_orientation += 90
    
    end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
    end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
    edge_point = (end_x, end_y)

def start_simulation(direction_of_movement1, amount_of_curve1, direction_of_turn1, amount_of_turn1, direction_of_movement2, amount_of_curve2, direction_of_turn2, amount_of_turn2, number_of_loops):
    global robot_orientation
    global robot_position
    global edge_point
    root = tk.Tk()
    generate_grid_points(grid_size, cell_size)
    canvas = tk.Canvas(root, width=grid_size*cell_size, height=grid_size*cell_size)
    canvas.pack()
    draw_grid(canvas)
    robot_position = (30, 370, 30)
    #robot_position = (370, 370, 30)
    robot_orientation = 90 # Initial orientation
    #robot_orientation = 270
    edge_point = (0,0)
    end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
    end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
    edge_point = (end_x, end_y)
    canvas.delete("all")
    grids_hit = []

    direction_of_movement = int(direction_of_movement1)
    amount_of_curve = int(amount_of_curve1)
    direction_of_turn = int(direction_of_turn1)
    amount_of_turn = int(amount_of_turn1)
    loops = int(number_of_loops)
    i = 1
    
    while (i < loops * 2):
        if direction_of_movement == 0:
            if amount_of_curve == 7:
                grids_hit.extend(curve_right_forward875(canvas))
            if amount_of_curve == 6:
                grids_hit.extend(curve_right_forward750(canvas))
            if amount_of_curve == 5:
                grids_hit.extend(curve_right_forward625(canvas))
            if amount_of_curve == 4:
                grids_hit.extend(curve_right_forward500(canvas))
            if amount_of_curve == 3:
                grids_hit.extend(curve_right_forward375(canvas))
            if amount_of_curve == 2:
                grids_hit.extend(curve_right_forward250(canvas))
            if amount_of_curve == 1:
                grids_hit.extend(curve_right_forward125(canvas))
            if amount_of_curve == 0:
                grids_hit.extend(curve_1000(canvas))
        
        elif direction_of_movement == 1:
            if amount_of_curve == 7:
                grids_hit.extend(curve_left_forward875(canvas))
            if amount_of_curve == 6:
                grids_hit.extend(curve_left_forward750(canvas))
            if amount_of_curve == 5:
                grids_hit.extend(curve_left_forward625(canvas))
            if amount_of_curve == 4:
                grids_hit.extend(curve_left_forward500(canvas))
            if amount_of_curve == 3:
                grids_hit.extend(curve_left_forward375(canvas))
            if amount_of_curve == 2:
                grids_hit.extend(curve_left_forward250(canvas))
            if amount_of_curve == 1:
                grids_hit.extend(curve_left_forward125(canvas))
            if amount_of_curve == 0:
                grids_hit.extend(curve_1000(canvas))
        
        if direction_of_turn == 0:
            turn_right(int(amount_of_turn))
        
        elif direction_of_turn == 1:
            turn_left(int(amount_of_turn))

        if i % 2 != 0:
            direction_of_movement = int(direction_of_movement2)
            amount_of_curve = int(amount_of_curve2)
            direction_of_turn = int(direction_of_turn2)
            amount_of_turn - int(amount_of_turn2)
        
        if i%2 == 0:
            direction_of_movement = int(direction_of_movement1)
            amount_of_curve = int(amount_of_curve1)
            direction_of_turn = int(direction_of_turn1)
            amount_of_turn = int(amount_of_turn1)
        
        i+=1
    return grids_hit

