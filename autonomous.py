from robomaster import robot
import time
 
def turn_one_wheel(robot_instance, speed, duration_seconds):
    """
    Simulate turning one wheel by setting differential speeds for a duration.
 
    :param robot_instance: The robot instance.
    :param speed: Speed at which to turn the wheel (positive for forward, negative for backward).
    :param duration_seconds: Duration to turn the wheel in seconds.
    """
    if robot_instance.is_moving:
        print("Error: Robot is already performing an action.")
        return
 
    try:
        robot_instance.is_moving = True
 
        # Simulate turning one wheel by setting differential speeds
        # Adjust speeds to simulate the effect of turning one wheel
        robot_instance.chassis.drive_speed(x=speed, y=0, z=0)
 
        # Wait for the specified duration
        time.sleep(duration_seconds)
 
    except Exception as e:
        print(f"Error occurred while turning wheel: {e}")
 
    finally:
        # Stop the chassis
        robot_instance.chassis.drive_speed(x=0, y=0, z=0)
        robot_instance.is_moving = False
 
def main():
    ep_core = robot.Robot()
    ep_core.is_moving = False
 
    try:
        ep_core.initialize()
 
        # Turn the robot by simulating wheel movement for 5 seconds at speed 30
        turn_one_wheel(ep_core, speed=30, duration_seconds=5)
 
    except Exception as e:
        print(f"Error occurred: {e}")
 
    finally:
        ep_core.close()
 
if __name__ == "__main__":
    main()