# Dynamixel-Async

High-level Python library for Dynamixel servos with async support.

## Features

- Async/await support for non-blocking operation
- High-level Pythonic interface
- Automatic model detection and configuration
- Unit conversion (degrees, RPM, etc.)
- Comprehensive error handling
- Support for multiple Dynamixel models

## Installation

```bash
pip install dynamixel-async
```

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dynamixel-async.git
cd dynamixel-async
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Basic Usage

```python
import asyncio
from dynamixel_async import DynamixelController

async def main():
    # Create controller instance
    controller = DynamixelController(baudrate=57600)
    
    # Connect and scan for servos
    await controller.connect()
    
    # Get servo with ID 1
    servo = controller.get_servo(1)
    if servo:
        # Move to 180 degrees
        servo.set_position(180.0)
        
        # Wait for movement to complete
        await controller.wait_for_servos()

if __name__ == "__main__":
    asyncio.run(main())
```

## Project Structure

```
src/
└── dynamixel_async/        # Main package
    ├── __init__.py        # Package initialization
    ├── constants.py       # Constants and enums
    ├── controller.py      # Main controller class
    ├── servo.py          # Servo interface
    └── models/           # Servo model definitions
        ├── __init__.py
        ├── base.py       # Base model class
        └── xm430.py      # XM430 model implementation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 