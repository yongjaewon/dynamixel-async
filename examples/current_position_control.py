"""Example of current-based position control with a Dynamixel servo."""

import asyncio
from dynamixel_async import DynamixelController


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
            
        # Example of position control with different current limits
        positions = [0, 180, 90, 270, 0]  # degrees
        currents = [100, 200, 300, 400, 500]  # mA
        
        for pos, current in zip(positions, currents):
            print(f"Moving to {pos} degrees with {current}mA current limit...")
            
            # Set position with current limit
            servo.set_current_based_position(pos, current)
            
            # Wait for movement to complete
            await controller.wait_for_servos()
            
            # Read current position and actual current
            actual_pos = servo.get_position()
            actual_current = servo.get_current()
            print(f"Position: {actual_pos:.1f}°, Current: {actual_current:.1f}mA")
            
            # Small delay between movements
            await asyncio.sleep(1.0)
            
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Clean up
        if controller:
            await controller.disconnect()


if __name__ == "__main__":
    asyncio.run(main()) 