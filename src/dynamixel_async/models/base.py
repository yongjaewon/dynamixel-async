"""
Base class for Dynamixel servo models.
"""

from typing import Dict, Set, Optional, Any
from ..constants import ControlTableItem, AccessType


class DynamixelModel:
    """Base class for all Dynamixel servo models."""
    
    MODEL_NUMBER: int = None
    PROTOCOL_VERSION: float = 2.0
    
    def __init__(self):
        """Initialize the model."""
        if self.MODEL_NUMBER is None:
            raise NotImplementedError("MODEL_NUMBER must be defined in subclass")
            
        self.control_table: Dict[str, ControlTableItem] = {}
        self.features: Set[str] = set()
        
    def get_register(self, name: str) -> Optional[ControlTableItem]:
        """Get a control table register by name."""
        return self.control_table.get(name)
        
    def validate_value(self, register_name: str, value: Any) -> bool:
        """
        Validate a value for a given register.
        
        Args:
            register_name: Name of the register
            value: Value to validate
            
        Returns:
            bool: True if value is valid for the register
            
        Raises:
            KeyError: If register_name doesn't exist
            ValueError: If value is invalid for the register
        """
        register = self.get_register(register_name)
        if not register:
            raise KeyError(f"Register {register_name} not found")
            
        if register.value_range is None:
            return True
            
        if len(register.value_range) == 1:
            # Single valid value
            return value == register.value_range[0]
        elif len(register.value_range) == 2:
            # Range of values
            min_val, max_val = register.value_range
            return min_val <= value <= max_val
            
        # List of valid values
        return value in register.value_range
        
    def has_feature(self, feature: str) -> bool:
        """Check if model supports a specific feature."""
        return feature in self.features
        
    def position_to_degrees(self, position: int) -> float:
        """Convert raw position value to degrees."""
        raise NotImplementedError
        
    def degrees_to_position(self, degrees: float) -> int:
        """Convert degrees to raw position value."""
        raise NotImplementedError
        
    def velocity_to_rpm(self, velocity: int) -> float:
        """Convert raw velocity value to RPM."""
        raise NotImplementedError
        
    def rpm_to_velocity(self, rpm: float) -> int:
        """Convert RPM to raw velocity value."""
        raise NotImplementedError
        
    def validate_register_access(self, register_name: str, is_write: bool = False) -> bool:
        """
        Validate if a register can be accessed in the specified mode.
        
        Args:
            register_name: Name of the register
            is_write: True if write access is required, False for read
            
        Returns:
            bool: True if access is allowed
            
        Raises:
            KeyError: If register_name doesn't exist
        """
        register = self.get_register(register_name)
        if not register:
            raise KeyError(f"Register {register_name} not found")
            
        if is_write:
            return register.access == AccessType.READ_WRITE
        return True  # All registers are readable


# Registry of supported models
SUPPORTED_MODELS: Dict[int, DynamixelModel] = {}


def register_model(model_class: type) -> None:
    """Register a Dynamixel model class."""
    instance = model_class()
    SUPPORTED_MODELS[instance.MODEL_NUMBER] = instance 