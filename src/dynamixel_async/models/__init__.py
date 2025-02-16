"""
Dynamixel servo model definitions.
"""

from .base import DynamixelModel, SUPPORTED_MODELS, register_model
from .xm430 import XM430W210Model

# Register supported models
register_model(XM430W210Model)

__all__ = [
    'DynamixelModel',
    'SUPPORTED_MODELS',
    'register_model',
    'XM430W210Model'
] 