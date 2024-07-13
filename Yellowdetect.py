import cv2
from robomaster import robot
import numpy as np

# Initialize the RoboMaster robot object
ep_robot = robot.Robot()
# Connect to the robot
ep_robot.initialize(conn_type="ap")
# Get the camera object
camera = ep_robot.camera
# Start the camera feed
camera.start_video_stream(display=False)
# Create a window to display the camera feed
cv2.namedWindow("RoboMaster EP1S Camera", cv2.WINDOW_NORMAL)

# Line following parameters
follow_speed = 0.05  # Speed to move forward while following the line
turn_scale = 0.125  # Scale factor to adjust the turning speed

def detect_yellow_line(frame):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define the yellow color range in HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    # Create a mask for the yellow color
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        # Search for the largest contour that represents the yellow line
        largest_contour = max(contours, key=cv2.contourArea)
        # Draw the yellow line as green
        cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
        # Calculate the center of the largest contour
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            # Follow the line based on the center position
            follow_line(cx, frame.shape[1])
        else:
            # Line not detected, stop the robot
            stop_robot()
    else:
        # Line not detected, stop the robot
        stop_robot()
    return frame

def follow_line(cx, frame_width):
    # Calculate the deviation from the center of the frame
    deviation = cx - (frame_width // 2)
    # Adjust the turning speed proportionally based on the deviation
    turn_speed = turn_scale * deviation
    # Drive the robot with the adjusted speeds
    ep_robot.chassis.drive_speed(x=follow_speed, z=turn_speed)

def stop_robot():
    # Stop the robot's movement
    ep_robot.chassis.drive_speed(x=0, z=0)

while True:
    # Get the latest frame from the camera
    frame = camera.read_cv2_image()
    # Crop a small area for line detection
    crop_top = frame.shape[0] * 2 // 3
    crop_bottom = frame.shape[0]
    crop_left = frame.shape[1] // 3
    crop_right = frame.shape[1] * 2 // 3
    cropped_frame = frame[crop_top:crop_bottom, crop_left:crop_right].copy()
    # Detect the yellow line in the cropped area
    processed_frame = detect_yellow_line(cropped_frame)
    # Show the frame in the window
    cv2.imshow("RoboMaster EP1S Camera", processed_frame)
    # Wait for a key press and check if it's 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the robot's movement
stop_robot()
# Stop the camera feed and release the camera
camera.stop_video_stream()
camera.close()
# Disconnect from the robot
ep_robot.close()
# Destroy all windows
cv2.destroyAllWindows()
