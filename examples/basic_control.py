"""Basic example of controlling a Dynamixel servo."""

import asyncio
from dynamixel_async import DynamixelController


async def main():
    # Create controller instance (auto-detects port)
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
            
        # Enable torque
        servo.enable_torque()
        
        # Move to different positions
        positions = [0, 90, 180, 90, 0]
        for pos in positions:
            print(f"Moving to {pos} degrees...")
            servo.set_position(pos)
            await controller.wait_for_servos()
            
            # Read current position
            current_pos = servo.get_position()
            print(f"Current position: {current_pos:.1f} degrees")
            await asyncio.sleep(1.0)
            
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Clean up
        if controller:
            await controller.disconnect()


if __name__ == "__main__":
    asyncio.run(main()) 