"""
Dynamixel-Async - High-level Python library for Dynamixel servos with async support.

A Pythonic interface for controlling Dynamixel servos with async support.
Provides high-level abstractions, auto-detection of servo models, and proper error handling.
"""

from .constants import AccessType, ControlTableItem, OperatingMode, Baudrate
from .models import (
    DynamixelModel,
    SUPPORTED_MODELS,
    register_model,
    XM430W210Model
)
from .exceptions import (
    DynamixelError,
    DynamixelConnectionError,
    DynamixelServoError,
    DynamixelTimeoutError,
    DynamixelModelError
)

__version__ = "0.1.0"
__all__ = [
    'DynamixelModel',
    'SUPPORTED_MODELS',
    'register_model',
    'XM430W210Model',
    'OperatingMode',
    'Baudrate',
    'AccessType',
    'ControlTableItem',
    'DynamixelError',
    'DynamixelConnectionError',
    'DynamixelServoError',
    'DynamixelTimeoutError',
    'DynamixelModelError'
] 