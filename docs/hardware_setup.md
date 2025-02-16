# Hardware Setup Guide

This guide will help you set up your Dynamixel servos for use with this library.

## Requirements

1. Dynamixel Servo(s)
   - Supported models: XM430-W210, XM430-W350, etc.
   - Make sure servos have unique IDs

2. Power Supply
   - 12V DC power supply (check your servo's specifications)
   - Adequate current rating (typically 1-2A per servo)

3. USB Interface
   - U2D2 or similar USB-to-TTL/RS485 converter
   - U2D2 Power Hub Board (recommended)

## Physical Setup

1. **Power Connection**
   ```
   Power Supply (12V) → U2D2 Power Hub → Servo
   ```

2. **Data Connection**
   ```
   Computer USB → U2D2 → Servo Data Port
   ```

3. **Daisy Chaining** (multiple servos)
   ```
   U2D2 → Servo 1 → Servo 2 → Servo 3 → ...
   ```

## Software Setup

1. Install USB drivers for your interface:
   - [FTDI drivers](https://ftdichip.com/drivers/) for U2D2
   - [Silicon Labs drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) for some other interfaces

2. Verify port detection:
   ```bash
   # Linux/macOS
   ls /dev/tty*

   # Windows
   # Check Device Manager under "Ports (COM & LPT)"
   ```

3. Install this library:
   ```bash
   pip install dynamixel-async
   ```

## Troubleshooting

### Common Issues

1. **Servo Not Responding**
   - Check power connections
   - Verify correct voltage
   - Check data cable connections
   - Try different baudrates

2. **Communication Errors**
   - Check USB drivers
   - Try unplugging/replugging USB
   - Check for loose connections
   - Verify correct protocol version

3. **Multiple Servo Issues**
   - Check for ID conflicts
   - Verify daisy-chain connections
   - Check total power requirements

### LED Status

The status LED on Dynamixel servos indicates various conditions:

- **Solid Green**: Normal operation
- **Blinking Green**: Processing instruction
- **Solid Red**: Hardware error
- **Blinking Red**: Overheating warning

## Safety Precautions

1. **Power**
   - Never exceed voltage limits
   - Connect/disconnect power when off
   - Use appropriate power supply

2. **Mechanical**
   - Don't force movement when powered
   - Respect position limits
   - Allow cooling between operations

3. **Electrical**
   - Don't short circuit connections
   - Keep connections clean and secure
   - Use proper wire gauge

## Next Steps

Once your hardware is set up:
1. Try the [basic example](../examples/basic_control.py)
2. Read the [Getting Started Guide](getting_started.md)
3. Check the [API Reference](api.md) for details 