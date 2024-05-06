import testcamera
import cv2
import time
import move

#NEED TO BE ABLE TO PASS MOVEMENT INSIDE GRID TRACKING
def gridtracking(direction_of_movement, amount_of_curve, direction_of_turn, amount_of_turn, number_of_loops):
    # Define the frame rate and the interval (in seconds) between captures
    # Set the maximum number of images to capture
    max_images = 106
    image_count = 0

    grids_hit = []

    # List to store captured images
    captured_images = []
    buffer_size = 20
    cap = cv2.VideoCapture('rtsp://admin:123456@136.244.195.47:554/Streaming/channels/0')  # Use 0 for the default camera
    cap.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)
    i = 0

    try:
        while i < number_of_loops:
            #move.grid_forward(0.2)
            if direction_of_movement == 0:
                if amount_of_curve == 0:
                    move.grid_forward(0.2)
                elif amount_of_curve == 1:
                    move.curve_right_while_forward125()
                elif amount_of_curve == 2:
                    move.curve_right_while_forward250()
                elif amount_of_curve == 3:
                    move.curve_right_while_forward375()
                elif amount_of_curve == 4:
                    move.curve_right_while_forward500()
                elif amount_of_curve == 5:
                    move.curve_right_while_forward625()
                elif amount_of_curve == 6:
                    move.curve_right_while_forward750()
                elif amount_of_curve == 7:
                    move.curve_right_while_forward875()
                elif amount_of_curve == 8:
                    move.curve_right_while_forward1000()

            #all left movement
            else:
                if amount_of_curve == 0:
                    move.grid_forward(0.2)
                elif amount_of_curve == 1:
                    move.curve_left_while_forward125()
                elif amount_of_curve == 2:
                    move.curve_left_while_forward250()
                elif amount_of_curve == 3:
                    move.curve_left_while_forward375()
                elif amount_of_curve == 4:
                    move.curve_left_while_forward500()
                elif amount_of_curve == 5:
                    move.curve_left_while_forward625()
                elif amount_of_curve == 6:
                    move.curve_left_while_forward750()
                elif amount_of_curve == 7:
                    move.curve_left_while_forward875()
                elif amount_of_curve == 8:
                    move.curve_left_while_forward1000()
        
            while image_count < max_images:
                ret, frame = cap.read()
                captured_images.append([ret, frame])
                image_count += 1
            
            move.stop()
            image_count = 0
            i += 1
            sharpness = 0.25 * amount_of_turn
            if direction_of_turn == 0:
                move.right(1, sharpness)
            elif direction_of_turn == 1:
                move.left(1, sharpness)

    finally:
        for i in range(len(captured_images)):
            if i % 15 == 0:
                # Display the image
                info = testcamera.calculate_orientation(captured_images[i][0], captured_images[i][1])
                print(info[0])
                grids_hit.append(testcamera.point_in_grid(info[0], info[2]))
                # Delay for a short time (adjust as needed)
                print(f"image {i} processed")
        return grids_hit