"""High-level interface for individual Dynamixel servos."""

import logging
from typing import Optional, Any, Dict, Tuple
from dynamixel_sdk.robotis_def import COMM_SUCCESS
from dynamixel_sdk.port_handler import PortHandler
from dynamixel_sdk.packet_handler import PacketHandler
from .constants import OperatingMode
from .models import DynamixelModel, SUPPORTED_MODELS
from .exceptions import DynamixelServoError, DynamixelModelError

logger = logging.getLogger(__name__)

class DynamixelServo:
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
        return self._write_to_address("TORQUE_ENABLE", 1)
        
    def disable_torque(self) -> bool:
        return self._write_to_address("TORQUE_ENABLE", 0)
        
    def set_position(self, position_degrees: float) -> bool:
        return self._write_to_address("GOAL_POSITION", position_degrees)
        
    def get_position(self) -> Optional[float]:
        return self._read_from_address("PRESENT_POSITION")
        
    def set_operating_mode(self, mode: OperatingMode) -> bool:
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
        
    def get_current(self) -> Optional[float]:
        if not self.model or not self.model.supports_feature("current_control"):
            raise DynamixelServoError(
                self.id,
                "Current reading not supported by this model"
            )
        return self._read_from_address("PRESENT_CURRENT")
        
    def set_current_limit(self, current_ma: float) -> bool:
        if not self.model or not self.model.supports_feature("current_control"):
            raise DynamixelServoError(
                self.id,
                "Current control not supported by this model"
            )
        return self._write_to_address("CURRENT_LIMIT", current_ma)
        
    def get_current_limit(self) -> Optional[float]:
        if not self.model or not self.model.supports_feature("current_control"):
            raise DynamixelServoError(
                self.id,
                "Current control not supported by this model"
            )
        return self._read_from_address("CURRENT_LIMIT")
        
    def get_model_info(self) -> Dict[str, Any]:
        if not self.model:
            raise DynamixelModelError("No model detected for this servo")
            
        return {
            "model_number": self.model.model_number,
            "name": self.model.name,
            "features": list(self.model.features)
        }

    def set_velocity(self, velocity_rpm: float) -> bool:
        return self._write_to_address("GOAL_VELOCITY", velocity_rpm)
        
    def get_velocity(self) -> Optional[float]:
        return self._read_from_address("PRESENT_VELOCITY")

    def set_pwm(self, pwm_value: int) -> bool:
        return self._write_to_address("GOAL_PWM", pwm_value)
        
    def get_pwm(self) -> Optional[int]:
        return self._read_from_address("PRESENT_PWM")

    def set_led(self, on: bool) -> bool:
        return self._write_to_address("LED", 1 if on else 0)

    def set_profile_velocity(self, velocity_rpm: float) -> bool:
        return self._write_to_address("PROFILE_VELOCITY", velocity_rpm)
        
    def set_profile_acceleration(self, acceleration: float) -> bool:
        return self._write_to_address("PROFILE_ACCELERATION", acceleration)
        
    def get_profile_velocity(self) -> Optional[float]:
        return self._read_from_address("PROFILE_VELOCITY")
        
    def get_profile_acceleration(self) -> Optional[float]:
        return self._read_from_address("PROFILE_ACCELERATION")

    def get_temperature(self) -> Optional[float]:
        return self._read_from_address("PRESENT_TEMPERATURE")
        
    def get_voltage(self) -> Optional[float]:
        return self._read_from_address("PRESENT_INPUT_VOLTAGE")
        
    def get_load(self) -> Optional[float]:
        return self._read_from_address("PRESENT_LOAD")
        
    def is_moving(self) -> bool:
        return bool(self._read_from_address("MOVING"))

    def set_position_gains(self, p: int, i: int = 0, d: int = 0) -> bool:
        success = True
        success &= self._write_to_address("POSITION_P_GAIN", p)
        success &= self._write_to_address("POSITION_I_GAIN", i)
        success &= self._write_to_address("POSITION_D_GAIN", d)
        return success
        
    def get_position_gains(self) -> Tuple[int, int, int]:
        p = self._read_from_address("POSITION_P_GAIN") or 0
        i = self._read_from_address("POSITION_I_GAIN") or 0
        d = self._read_from_address("POSITION_D_GAIN") or 0
        return (p, i, d)
        
    def set_velocity_gains(self, p: int, i: int = 0) -> bool:
        success = True
        success &= self._write_to_address("VELOCITY_P_GAIN", p)
        success &= self._write_to_address("VELOCITY_I_GAIN", i)
        return success
        
    def get_velocity_gains(self) -> Tuple[int, int]:
        p = self._read_from_address("VELOCITY_P_GAIN") or 0
        i = self._read_from_address("VELOCITY_I_GAIN") or 0
        return (p, i) 