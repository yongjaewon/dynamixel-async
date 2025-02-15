"""
DynaPy - High-level Python library for Dynamixel servos

A Pythonic interface for controlling Dynamixel servos with async support.
Provides high-level abstractions, auto-detection of servo models, and proper error handling.
"""

from .constants import OperatingMode, Baudrate, AccessType
from .controller import DynamixelController
from .servo import DynamixelServo
from .models import (
    DynamixelModel,
    XM430W210,
    SUPPORTED_MODELS,
    register_model
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
    'DynamixelController',
    'DynamixelServo',
    'DynamixelModel',
    'XM430W210',
    'SUPPORTED_MODELS',
    'register_model',
    'OperatingMode',
    'Baudrate',
    'AccessType',
    'DynamixelError',
    'DynamixelConnectionError',
    'DynamixelServoError',
    'DynamixelTimeoutError',
    'DynamixelModelError'
] 