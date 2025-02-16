"""Example of velocity control with a Dynamixel servo."""

import asyncio
from dynamixel_async import DynamixelController, OperatingMode


async def main():
    # Create controller instance
    controller = DynamixelController(baudrate=57600)
    
    try:
        # Connect and scan for servos
        await controller.connect()
        print(f"Connected servos: {controller.get_connected_ids()}")
        
        # Get first servo
        servo = controller.get_servo(1)
        if not servo:
            print("No servo found with ID 1")
            return
            
        # Set to velocity mode
        servo.set_operating_mode(OperatingMode.VELOCITY)
        servo.enable_torque()
        
        # Rotate at different speeds
        speeds = [10, 20, 30, 0, -10, -20, -30, 0]  # RPM
        for speed in speeds:
            print(f"Setting velocity to {speed} RPM...")
            servo.set_velocity(speed)
            
            # Run for 2 seconds
            await asyncio.sleep(2.0)
            
            # Read current velocity
            current_speed = servo.get_velocity()
            print(f"Current velocity: {current_speed:.1f} RPM")
            
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Stop and clean up
        if servo:
            servo.set_velocity(0)
        if controller:
            await controller.disconnect()


if __name__ == "__main__":
    asyncio.run(main()) 