"""High-level interface for individual Dynamixel servos."""

import logging
from typing import Optional, Any, Dict
from dynamixel_sdk.robotis_def import COMM_SUCCESS
from dynamixel_sdk.port_handler import PortHandler
from dynamixel_sdk.packet_handler import PacketHandler
from .constants import OperatingMode
from .models import DynamixelModel, SUPPORTED_MODELS
from .exceptions import DynamixelServoError, DynamixelModelError

logger = logging.getLogger(__name__)

class DynamixelServo:
    """
    High-level interface for a single Dynamixel servo.
    
    Provides a Pythonic interface for controlling Dynamixel servos,
    with automatic unit conversion and error handling.
    """
    
    def __init__(
        self,
        port_handler: PortHandler,
        packet_handler: PacketHandler,
        servo_id: int,
        model: Optional[DynamixelModel] = None
    ):
        self.port_handler = port_handler
        self.packet_handler = packet_handler
        self.id = servo_id
        self.model = model
        
    @classmethod
    async def detect_model(
        cls,
        port_handler: PortHandler,
        packet_handler: PacketHandler,
        servo_id: int
    ) -> Optional[DynamixelModel]:
        """
        Detect servo model by reading model number.
        
        Args:
            port_handler: Dynamixel port handler
            packet_handler: Dynamixel packet handler
            servo_id: ID of the servo to detect
            
        Returns:
            DynamixelModel if detected, None if not found or error
        """
        try:
            # Create temporary servo instance to read model number
            temp_servo = cls(port_handler, packet_handler, servo_id)
            model_number = await temp_servo._read_from_address("MODEL_NUMBER")
            if model_number in SUPPORTED_MODELS:
                return SUPPORTED_MODELS[model_number]
            logger.warning(f"Unknown model number: {model_number}")
            return None
        except Exception as e:
            logger.debug(f"Could not detect model for servo {servo_id}: {e}")
            return None
            
    def _write_to_address(self, item_name: str, value: Any) -> bool:
        """
        Write a value to a control table address with proper conversion.
        
        Args:
            item_name: Name of the control table item
            value: Value to write (in high-level units)
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            DynamixelServoError: If write operation fails
        """
        try:
            if not self.model:
                raise DynamixelModelError("No model detected for this servo")
                
            item = self.model.get_control_table_item(item_name)
            
            if not item.validate_value(value):
                raise ValueError(f"Value {value} is outside valid range for {item_name}")
                
            # Convert value if needed
            if item.value_converter:
                value = item.value_converter(value)
                
            # Choose write function based on size
            if item.size == 1:
                result, error = self.packet_handler.write1ByteTxRx(
                    self.port_handler, self.id, item.address, value)
            elif item.size == 2:
                result, error = self.packet_handler.write2ByteTxRx(
                    self.port_handler, self.id, item.address, value)
            elif item.size == 4:
                result, error = self.packet_handler.write4ByteTxRx(
                    self.port_handler, self.id, item.address, value)
            else:
                raise ValueError(f"Unsupported item size: {item.size}")
                
            if result != COMM_SUCCESS:
                raise DynamixelServoError(
                    self.id,
                    f"Failed to write {item_name}: {self.packet_handler.getTxRxResult(result)}"
                )
            if error != 0:
                raise DynamixelServoError(
                    self.id,
                    f"Servo error writing {item_name}: {self.packet_handler.getRxPacketError(error)}"
                )
                
            return True
            
        except Exception as e:
            logger.error(f"Error writing to servo {self.id}: {str(e)}")
            raise DynamixelServoError(self.id, str(e))
            
    def _read_from_address(self, item_name: str) -> Optional[Any]:
        """
        Read a value from a control table address with proper conversion.
        
        Args:
            item_name: Name of the control table item
            
        Returns:
            The read value (in high-level units)
            
        Raises:
            DynamixelServoError: If read operation fails
        """
        try:
            if not self.model:
                raise DynamixelModelError("No model detected for this servo")
                
            item = self.model.get_control_table_item(item_name)
            
            # Choose read function based on size
            if item.size == 1:
                result, value, error = self.packet_handler.read1ByteTxRx(
                    self.port_handler, self.id, item.address)
            elif item.size == 2:
                result, value, error = self.packet_handler.read2ByteTxRx(
                    self.port_handler, self.id, item.address)
            elif item.size == 4:
                result, value, error = self.packet_handler.read4ByteTxRx(
                    self.port_handler, self.id, item.address)
            else:
                raise ValueError(f"Unsupported item size: {item.size}")
                
            if result != COMM_SUCCESS:
                raise DynamixelServoError(
                    self.id,
                    f"Failed to read {item_name}: {self.packet_handler.getTxRxResult(result)}"
                )
            if error != 0:
                raise DynamixelServoError(
                    self.id,
                    f"Servo error reading {item_name}: {self.packet_handler.getRxPacketError(error)}"
                )
                
            # Convert value if needed
            if item.value_converter and value is not None:
                value = item.value_converter(value)
                
            return value
            
        except Exception as e:
            logger.error(f"Error reading from servo {self.id}: {str(e)}")
            raise DynamixelServoError(self.id, str(e))
            
    # High-level control methods
    def enable_torque(self) -> bool:
        """Enable torque for the servo."""
        return self._write_to_address("TORQUE_ENABLE", 1)
        
    def disable_torque(self) -> bool:
        """Disable torque for the servo."""
        return self._write_to_address("TORQUE_ENABLE", 0)
        
    def set_position(self, position_degrees: float) -> bool:
        """
        Set the goal position in degrees (0-360).
        
        Args:
            position_degrees: Target position in degrees
            
        Returns:
            bool: True if successful
        """
        return self._write_to_address("GOAL_POSITION", position_degrees)
        
    def get_position(self) -> Optional[float]:
        """
        Get the current position in degrees.
        
        Returns:
            float: Current position in degrees
        """
        return self._read_from_address("PRESENT_POSITION")
        
    def set_operating_mode(self, mode: OperatingMode) -> bool:
        """
        Set the operating mode of the servo.
        
        Args:
            mode: Desired operating mode
            
        Returns:
            bool: True if successful
            
        Raises:
            DynamixelServoError: If mode is not supported by this model
        """
        if not self.model:
            raise DynamixelModelError("No model detected for this servo")
            
        mode_feature_map = {
            OperatingMode.CURRENT: "current_control",
            OperatingMode.VELOCITY: "velocity_control",
            OperatingMode.POSITION: "position_control",
            OperatingMode.EXTENDED_POSITION: "extended_position",
            OperatingMode.CURRENT_BASED_POSITION: "current_based_position",
            OperatingMode.PWM: "pwm_control"
        }
        
        feature = mode_feature_map.get(mode)
        if not feature or not self.model.supports_feature(feature):
            raise DynamixelServoError(
                self.id,
                f"Operating mode {mode.name} not supported by {self.model.name}"
            )
            
        return self._write_to_address("OPERATING_MODE", mode)
        
    def set_current_limit(self, current_ma: float) -> bool:
        """
        Set the current limit in milliamps.
        
        Args:
            current_ma: Current limit in milliamps
            
        Returns:
            bool: True if successful
            
        Raises:
            DynamixelServoError: If current control is not supported
        """
        if not self.model or not self.model.supports_feature("current_control"):
            raise DynamixelServoError(self.id, "Current control not supported by this model")
        return self._write_to_address("CURRENT_LIMIT", current_ma)
        
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about this servo's model."""
        if not self.model:
            raise DynamixelModelError("No model detected for this servo")
            
        return {
            "model_number": self.model.model_number,
            "name": self.model.name,
            "features": list(self.model.features)
        } 