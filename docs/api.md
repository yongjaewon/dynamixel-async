# Dynamixel-Async API Reference

## Core Classes

### DynamixelController

The main interface for communicating with Dynamixel servos.

```python
from dynamixel_async import DynamixelController

controller = DynamixelController(
    port=None,  # Auto-detect port
    baudrate=57600,
    protocol_version=2.0
)
```

#### Methods

- `async connect() -> None`: Initialize connection to servos
- `async disconnect() -> None`: Close connection
- `get_servo(id: int) -> Optional[DynamixelServo]`: Get servo by ID
- `get_connected_ids() -> List[int]`: Get list of connected servo IDs
- `async wait_for_servos(timeout: float = 5.0) -> bool`: Wait for servo movements to complete

### DynamixelServo

Represents a single Dynamixel servo motor.

```python
from dynamixel_async import DynamixelServo

# Get servo instance from controller
servo = controller.get_servo(1)
```

#### Methods

- `enable_torque() -> bool`: Enable servo torque
- `disable_torque() -> bool`: Disable servo torque
- `set_position(position: float) -> bool`: Set target position in degrees
- `get_position() -> float`: Get current position in degrees
- `set_velocity(velocity: float) -> bool`: Set velocity in RPM
- `get_velocity() -> float`: Get current velocity in RPM
- `set_operating_mode(mode: OperatingMode) -> bool`: Set servo operating mode

### OperatingMode

Enum defining servo operating modes.

```python
from dynamixel_async import OperatingMode

# Available modes
OperatingMode.POSITION       # Position control mode
OperatingMode.VELOCITY      # Velocity control mode
OperatingMode.PWM           # PWM control mode
OperatingMode.CURRENT       # Current control mode
OperatingMode.EXTENDED_POS  # Extended position control mode
```

## Error Handling

### Exception Classes

```python
from dynamixel_async import (
    DynamixelError,           # Base exception class
    DynamixelConnectionError, # Connection-related errors
    DynamixelTimeoutError,    # Timeout errors
    DynamixelHardwareError,   # Hardware-related errors
    DynamixelChecksumError    # Checksum validation errors
)
```

## Models

### DynamixelModel

Base class for defining Dynamixel servo models.

```python
from dynamixel_async import DynamixelModel, register_model
from dynamixel_async.constants import ControlTableItem, AccessType

class CustomModel(DynamixelModel):
    def __init__(self):
        super().__init__(
            model_number=1234,
            name="Custom-Model",
            features={"position_control"}
        )
        
        self.control_table_overrides = {
            "POSITION_P_GAIN": ControlTableItem(
                84, 2, AccessType.READ_WRITE,
                "Position P Gain",
                value_range=(0, 16383),
                units=None,
                default=800
            )
        }

# Register custom model
register_model(CustomModel())
```

## Constants

### Control Table Items

```python
from dynamixel_async.constants import ControlTableItem

# Standard control table items
TORQUE_ENABLE = ControlTableItem(
    64, 1, AccessType.READ_WRITE,
    "Torque Enable",
    value_range=(0, 1),
    units=None,
    default=0
)
```

### Access Types

```python
from dynamixel_async.constants import AccessType

AccessType.READ_ONLY    # Read-only register
AccessType.READ_WRITE   # Read-write register
```

## Utilities

### Conversion Functions

```python
from dynamixel_async.utils import (
    degrees_to_position,  # Convert degrees to raw position value
    position_to_degrees,  # Convert raw position to degrees
    rpm_to_velocity,      # Convert RPM to raw velocity value
    velocity_to_rpm       # Convert raw velocity to RPM
)
```

## Advanced Usage

### Context Manager

```python
from dynamixel_async import DynamixelController

async with DynamixelController() as controller:
    servo = controller.get_servo(1)
    if servo:
        servo.set_position(180.0)
        await controller.wait_for_servos()
```

### Bulk Operations

```python
# Set multiple servo positions simultaneously
positions = {
    1: 180.0,  # Servo ID 1 -> 180 degrees
    2: 90.0,   # Servo ID 2 -> 90 degrees
    3: 45.0    # Servo ID 3 -> 45 degrees
}

controller.set_positions(positions)
await controller.wait_for_servos()
```

## Configuration

### Global Settings

```python
from dynamixel_async import set_global_config

set_global_config(
    default_baudrate=57600,
    default_protocol=2.0,
    timeout=1.0,
    retry_count=3
)
```

For more examples and detailed usage, see the [Getting Started Guide](getting_started.md). 