import time
from robomaster import robot
from robomaster import led

# Global variable to store the distance to the nearest obstacle
obstacle_distance = 1000

# Global variable to store the start time of the timer
start_time = None

def sub_data_handler(sub_info):
    """
    Callback function to handle distance sensor data.
    
    :param sub_info: Distance information from the sensor.
    """
    global obstacle_distance
    distance = sub_info
    obstacle_distance = distance[0]
    print(f"Object detected at a distance of {obstacle_distance} mm")

def timer_expired(duration):
    """
    Function to check if the timer has expired.
    
    :param duration: Duration of the timer in seconds.
    :return: True if the timer has expired, False otherwise.
    """
    global start_time
    if start_time is None:
        return False
    return time.time() - start_time >= duration

if __name__ == '__main__':
    # Initialize the robot
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_led = ep_robot.led
    ep_sensor = ep_robot.sensor
    speed = 0.2  # Adjust the speed as needed
    
    try:
        # Subscribe to distance data with a frequency of 5 Hz and set the callback function
        ep_sensor.sub_distance(freq=5, callback=sub_data_handler)
        
        # Start the timer
        start_time = time.time()
        
        while True:
            # Check if timer has expired
            if timer_expired(40):
                print("Timer expired! Stopping the robot.")
                ep_robot.chassis.drive_speed(x=0, y=0, z=0)
                break
            
            # Check obstacle distance and take action
            if obstacle_distance > 400:  # If the obstacle is beyond 40 cm (400 mm)
                # Green light when moving
                ep_led.set_led(comp=led.COMP_ALL, r=0, g=255, b=0, effect=led.EFFECT_ON)
                # Move forward
                ep_robot.chassis.drive_speed(x=speed, y=0, z=0)
            else:
                # Red light when obstacle detected
                ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_ON)
                # Stop and avoid the obstacle
                ep_robot.chassis.drive_speed(x=0, y=0, z=0)  # Ensure the robot stops
                time.sleep(0.5)
                # Move sideways to avoid the obstacle
                ep_robot.chassis.drive_speed(x=0, y=(2.5 * speed), z=0)
                time.sleep(1)
                # Continue moving forward along the x-axis
                ep_robot.chassis.drive_speed(x=(2.5 * speed), y=0, z=0)
                time.sleep(2.5)
                ep_robot.chassis.drive_speed(x=0, y=-(2.5 * speed), z=0)
                time.sleep(1)
            
            time.sleep(0.1)  # Adjust this sleep time as needed for smoother operation
    
    except Exception as e:
        print(f"Error occurred: {e}")
    
    finally:
        # Unsubscribe from the distance sensor data and close the robot
        ep_sensor.unsub_distance()
        ep_robot.close()
