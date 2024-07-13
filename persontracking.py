import cv2
import numpy as np
from robomaster import robot
import time

# Initialize YOLOv3 Tiny for person detection
net = cv2.dnn.readNet('yolov3-tiny.weights', 'yolov3-tiny.cfg')
classes = []
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Initialize DJI Robomaster
robomaster = robot.Robot()
robomaster.initialize(conn_type='ap')  # Assuming you are using Access Point mode

# Start video streaming
robomaster.camera.start_video_stream(display=False)

# Tracking parameters
follow_speed = 0.2  # Speed to move forward while tracking
turn_scale = 0.005  # Scale factor to adjust the turning speed
frame_center = (0, 0)  # Initial frame center (x, y)

# PID control parameters
kp = 0.1
ki = 0.01
kd = 0.05

# Initialize PID variables
integral_x = 0
last_error_x = 0
integral_z = 0
last_error_z = 0

# Set target frame size
target_frame_width = 320
target_frame_height = 240

while True:
    try:
        frame = robomaster.camera.read_cv2_image(strategy='newest')
    except queue.Empty:
        continue

    if frame is None:
        continue

    # Resize frame to target size
    frame = cv2.resize(frame, (target_frame_width, target_frame_height))
    height, width, channels = frame.shape

    # Resize frame to 416x416 for YOLOv3 Tiny input
    resized_frame = cv2.resize(frame, (416, 416))

    # Detecting objects
    blob = cv2.dnn.blobFromImage(resized_frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Initialize variables for tracking
    person_detected = False

    # Variables to store detected person's position
    person_x = 0
    person_width = 0

    # Processing each detected object
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # class_id 0 for person in COCO dataset
                # Object detected (person)
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Calculating bounding box coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Draw rectangle and label on the frame
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Person", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Update tracking center position
                frame_center = (center_x, center_y)
                person_detected = True

                # Store person's position and width
                person_x = center_x
                person_width = w

    # Perform tracking based on the detection
    if person_detected:
        # Calculate deviation from the center of the frame
        deviation_x = person_x - (width // 2)
        deviation_z = deviation_x / (width // 2)  # Normalize deviation

        # Update PID variables
        integral_x = integral_x + deviation_x
        derivative_x = deviation_x - last_error_x
        last_error_x = deviation_x

        integral_z = integral_z + deviation_z
        derivative_z = deviation_z - last_error_z
        last_error_z = deviation_z

        # Calculate PID control outputs
        x_speed = kp * deviation_x + ki * integral_x + kd * derivative_x
        z_speed = kp * deviation_z + ki * integral_z + kd * derivative_z

        # Limit x_speed and z_speed to reasonable values
        x_speed = np.clip(x_speed, -0.5, 0.5)  # Limit speed to +/- 0.5 m/s
        z_speed = np.clip(z_speed, -0.5, 0.5)  # Limit turning speed to +/- 0.5 rad/s

        # Print PID debug information
        print(f"Deviation X: {deviation_x}, Deviation Z: {deviation_z}")
        print(f"X Speed: {x_speed}, Z Speed: {z_speed}")

        # Drive the robot with adjusted speeds
        try:
            robomaster.chassis.drive_speed(x=follow_speed, z=-z_speed)  # Invert z_speed if necessary
            print(f"Drive Command - X Speed: {follow_speed}, Z Speed: {-z_speed}")
        except Exception as e:
            print(f"Error in sending drive command: {e}")
    else:
        # If no person detected, stop the robot
        try:
            robomaster.chassis.drive_speed(x=0, z=0)
        except Exception as e:
            print(f"Error in stopping robot: {e}")

    # Display the frame
    cv2.imshow('Person Detection and Tracking - RoboMaster EP1S Camera', frame)

    key = cv2.waitKey(1)
    if key == 27:  # press 'Esc' to exit
        break

# Clean up
robomaster.camera.stop_video_stream()
cv2.destroyAllWindows()
robomaster.close()
