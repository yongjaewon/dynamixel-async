"""
Constants and data structures for Dynamixel servo control.
"""

from enum import Enum, IntEnum
from dataclasses import dataclass
from typing import Optional, Tuple, Any


# Protocol versions
PROTOCOL_1 = 1.0
PROTOCOL_2 = 2.0

# Common values
BROADCAST_ID = 254  # Used to broadcast to all servos
MAX_ID = 252       # Maximum servo ID
DEFAULT_ID = 1     # Default servo ID

# Error bits
ERROR_NONE = 0x00
ERROR_RESULT_FAIL = 0x01
ERROR_INSTRUCTION = 0x02
ERROR_CRC = 0x03
ERROR_DATA_RANGE = 0x04
ERROR_DATA_LENGTH = 0x05
ERROR_DATA_LIMIT = 0x06
ERROR_ACCESS = 0x07


class AccessType(Enum):
    """Access type for control table items."""
    READ_ONLY = 'R'
    READ_WRITE = 'RW'


class OperatingMode(IntEnum):
    """Operating modes for Dynamixel servos."""
    CURRENT = 0
    VELOCITY = 1
    POSITION = 3
    EXTENDED_POSITION = 4
    CURRENT_BASED_POSITION = 5
    PWM = 16


class Baudrate(IntEnum):
    """Standard baudrates for Dynamixel communication."""
    BAUD_9600 = 0
    BAUD_57600 = 1
    BAUD_115200 = 2
    BAUD_1M = 3
    BAUD_2M = 4
    BAUD_3M = 5
    BAUD_4M = 6
    BAUD_4_5M = 7

    @property
    def value_bps(self) -> int:
        """Get the actual baudrate in bits per second."""
        return {
            0: 9600,
            1: 57600,
            2: 115200,
            3: 1000000,
            4: 2000000,
            5: 3000000,
            6: 4000000,
            7: 4500000
        }[self.value]


@dataclass
class ControlTableItem:
    """
    Represents an item in the Dynamixel control table.
    
    Args:
        address: Register address
        size: Size in bytes
        access: Access type (read-only or read-write)
        description: Human-readable description
        value_range: Valid value range (min, max) or specific values
        units: Units of measurement (if applicable)
        default: Default value
    """
    address: int
    size: int
    access: AccessType
    description: str
    value_range: Optional[Tuple[Any, ...]] = None
    units: Optional[str] = None
    default: Any = None 