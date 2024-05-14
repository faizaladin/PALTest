import tkinter as tk
import random
import time
import math

grid_points = {}  # Define grid_points as a global variable
grid_size = 5
cell_size = 80
robot_position = (40, 360, 30)
robot_orientation = 90 # Initial orientation
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
            robot_position = (robot_position[1], robot_position[2], robot_position[2])
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            return grids_hit
        if (edge_point[1] > max_y):
            robot_position = (robot_position[0], max_y - robot_position[1], robot_position[2])
            end_x = robot_position[0] + robot_position[2] * math.sin(math.radians(robot_orientation))
            end_y = robot_position[1] - robot_position[2] * math.cos(math.radians(robot_orientation))  # Negative because y-axis is inverted in tkinter
            edge_point = (end_x, end_y)
            return grids_hit
        # Redraw the grid with the new position
        canvas.delete("all")  # Clear the canvas
        draw_grid(canvas)
        
        # Update the current step
        curr_step += step
        
        # Update the canvas to visualize each step
        canvas.update()
        time.sleep(0.1)  # Adjust the sleep duration as needed
    return grids_hit

# Call the forward function to start moving the robot forward
# Keep the GUI running


root = tk.Tk()
generate_grid_points(grid_size, cell_size)
canvas = tk.Canvas(root, width=grid_size*cell_size, height=grid_size*cell_size)
canvas.pack()
draw_grid(canvas)
print(find_robot_grid(robot_position, grid_points))
print(forward(canvas, 400))
#print(edge_point)
#create_circle(40, 360, 20, canvas)
root.mainloop()