# Person Tracking and Object Detection using Robomaster EP Core and YOLOv3

This project involves developing an advanced system for person tracking and object detection using the **Robomaster EP Core** robot and **YOLOv3**. As part of my second semester course project for my Master's program, I undertook this project to explore the integration of robotics and computer vision. The project was divided into three main objectives: moving the robot from point A to point B, detecting and avoiding objects, and tracking a person.

## Project Objectives

1. **Move the Robot from Point A to Point B**
    - The first objective was to program the Robomaster EP Core to navigate autonomously from a predefined starting point (Point A) to a destination (Point B). This involved utilizing the robot's built-in motion control capabilities and sensors to ensure accurate and efficient movement.

2. **Detect and Avoid Objects using YOLOv8 and Sensors**
    - The second objective focused on enhancing the robot's navigation capabilities by integrating object detection and avoidance. YOLOv8, a state-of-the-art object detection model, was employed to identify obstacles in the robot's path. The robot's sensors were used to measure the distance to these objects and adjust the path to avoid collisions.

3. **Track a Person**
    - The third objective was to develop a system for tracking a person. YOLOv8 was again utilized to detect and identify a specific person. The Robomaster EP Core then used this information to follow the person, maintaining a safe distance and adjusting its trajectory in real-time.

## Tools and Technologies

- **Anaconda**: Used as the primary Python distribution and package manager, facilitating the setup of the development environment.
- **Visual Studio Code**: Employed as the integrated development environment (IDE) for coding and debugging.
- **Robomaster SDK**: Provided the necessary APIs and tools to control the Robomaster EP Core and integrate it with the object detection and tracking systems.
- **YOLOv8**: Leveraged for its powerful real-time object detection capabilities, enabling the robot to detect and avoid obstacles, as well as track a person.

## Project Workflow

1. **Setup and Configuration**
    - Anaconda was used to create a virtual environment, ensuring all dependencies and packages required for the project were installed and managed efficiently.
    - Visual Studio Code was configured with the necessary extensions and tools for Python development.

2. **Robot Navigation (Point A to Point B)**
    - Using the Robomaster SDK, a path was programmed for the robot to follow from Point A to Point B. The robot's sensors were utilized to ensure accurate navigation and obstacle avoidance.

3. **Object Detection and Avoidance**
    - YOLOv8 was integrated into the system to detect objects in the robot's path. The detected objects' coordinates were used in conjunction with the robot's sensors to calculate the distance and adjust the robot's path to avoid collisions.

4. **Person Tracking**
    - YOLOv8 was trained to detect and identify a specific person. The Robomaster EP Core was programmed to follow the person, using real-time data from the detection model to adjust its movement and maintain a safe distance.

## Results and Conclusion

The project successfully met all three objectives. The Robomaster EP Core was able to autonomously navigate from Point A to Point B, detect and avoid objects in its path, and effectively track a person. The integration of YOLOv8 with the Robomaster SDK proved to be a powerful combination, enabling advanced object detection and tracking capabilities. This project demonstrates the potential of combining robotics with computer vision for creating intelligent and autonomous systems.

## Future Work

Future improvements could include:
- Enhancing the robustness of the object detection and tracking system in various lighting conditions.
- Implementing more sophisticated path planning algorithms to improve navigation efficiency.
- Expanding the system to track multiple objects or people simultaneously.

---

