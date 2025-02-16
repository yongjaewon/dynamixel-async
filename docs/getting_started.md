# Getting Started with Dynamixel-Async

This guide will help you get started with the Dynamixel-Async library.

## Installation

1. Install the package using pip:
```bash
pip install dynamixel-async
```

2. Ensure you have the USB-to-Serial converter drivers installed for your operating system.

## Basic Usage

### Connecting to Servos

```python
import asyncio
from dynamixel_async import DynamixelController

async def main():
    # Create controller instance
    controller = DynamixelController(baudrate=57600)
    
    # Connect and scan for servos
    await controller.connect()
    
    # Print connected servo IDs
    print(f"Found servos: {controller.get_connected_ids()}")

asyncio.run(main())
```

### Position Control

```python
from dynamixel_async import DynamixelController, OperatingMode

async def position_control():
    controller = DynamixelController(baudrate=57600)
    await controller.connect()
    
    # Get servo with ID 1
    servo = controller.get_servo(1)
    if servo:
        # Set to position control mode
        servo.set_operating_mode(OperatingMode.POSITION)
        
        # Enable torque
        servo.enable_torque()
        
        # Move to 180 degrees
        servo.set_position(180.0)
        
        # Wait for movement to complete
        await controller.wait_for_servos(timeout=5.0)
        
        # Get current position
        current_pos = servo.get_position()
        print(f"Current position: {current_pos} degrees")

asyncio.run(position_control())
```

### Error Handling

```python
from dynamixel_async import (
    DynamixelError, DynamixelConnectionError,
    DynamixelTimeoutError
)

async def safe_control():
    try:
        controller = DynamixelController(baudrate=57600)
        await controller.connect()
        
        servo = controller.get_servo(1)
        if not servo:
            print("Servo not found")
            return
            
        servo.set_position(180.0)
        
    except DynamixelConnectionError as e:
        print(f"Connection error: {e}")
    except DynamixelTimeoutError as e:
        print(f"Timeout error: {e}")
    except DynamixelError as e:
        print(f"General error: {e}")
```

## Advanced Usage

### Custom Models

You can add support for additional Dynamixel models by subclassing `DynamixelModel`:

```python
from dynamixel_async import DynamixelModel, register_model
from dynamixel_async.constants import ControlTableItem, AccessType

class XL430W250(DynamixelModel):
    def __init__(self):
        super().__init__(
            model_number=1060,
            name="XL430-W250",
            features={
                "current_control",
                "velocity_control",
                "position_control",
                "extended_position",
                "pwm_control"
            }
        )
        
        # Add model-specific control table overrides
        self.control_table_overrides = {
            "CURRENT_LIMIT": ControlTableItem(
                38, 2, AccessType.READ_WRITE,
                "Maximum Current Limit",
                value_range=(0, 1193),
                units="mA",
                default=1193
            )
        }

# Register the new model
register_model(XL430W250())
```

### Velocity Control

```python
async def velocity_control():
    controller = DynamixelController(baudrate=57600)
    await controller.connect()
    
    servo = controller.get_servo(1)
    if servo:
        # Set to velocity control mode
        servo.set_operating_mode(OperatingMode.VELOCITY)
        
        # Enable torque
        servo.enable_torque()
        
        # Set velocity to 10 RPM
        servo.set_velocity(10.0)
        
        # Wait 5 seconds
        await asyncio.sleep(5.0)
        
        # Stop
        servo.set_velocity(0.0)
```

## Best Practices

1. Always use proper error handling with try/except blocks
2. Close the connection when done using `await controller.disconnect()`
3. Use the `async with` pattern when possible
4. Check return values from servo commands
5. Use proper type hints for better code safety

## Troubleshooting

Common issues and solutions:

1. **Cannot find servo port**
   - Check USB connection
   - Verify driver installation
   - Try different baudrates

2. **Communication errors**
   - Check wiring
   - Verify power supply
   - Check baudrate settings

3. **Servo not responding**
   - Verify ID settings
   - Check if torque is enabled
   - Verify operating mode

For more detailed information, see the [API Reference](api.md). 