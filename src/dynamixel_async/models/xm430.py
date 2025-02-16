"""
Control table definitions for XM430-W210/W350 DYNAMIXEL servos.
Reference: https://emanual.robotis.com/docs/en/dxl/x/xm430-w210/
"""

from ..constants import ControlTableItem, AccessType, PROTOCOL_2
from .base import DynamixelModel

# EEPROM Area (Persisted even after power cycle)
EEPROM_REGISTERS = {
    "MODEL_NUMBER": ControlTableItem(
        0, 2, AccessType.READ_ONLY,
        "Model Number",
        value_range=(1030,),  # XM430-W210 model number
        units=None,
        default=1030
    ),
    "MODEL_INFORMATION": ControlTableItem(
        2, 4, AccessType.READ_ONLY,
        "Model Information",
        value_range=None,
        units=None,
        default=None
    ),
    "FIRMWARE_VERSION": ControlTableItem(
        6, 1, AccessType.READ_ONLY,
        "Firmware Version",
        value_range=None,
        units=None,
        default=None
    ),
    "ID": ControlTableItem(
        7, 1, AccessType.READ_WRITE,
        "DYNAMIXEL ID",
        value_range=(0, 252),
        units=None,
        default=1
    ),
    "BAUD_RATE": ControlTableItem(
        8, 1, AccessType.READ_WRITE,
        "Communication Speed",
        value_range=(0, 7),
        units="bps",
        default=1  # 57600 bps
    ),
    "RETURN_DELAY_TIME": ControlTableItem(
        9, 1, AccessType.READ_WRITE,
        "Response Delay Time",
        value_range=(0, 254),
        units="2 usec",
        default=250  # 500us
    ),
    "DRIVE_MODE": ControlTableItem(
        10, 1, AccessType.READ_WRITE,
        "Drive Mode",
        value_range=(0, 5),
        units=None,
        default=0
    ),
    "OPERATING_MODE": ControlTableItem(
        11, 1, AccessType.READ_WRITE,
        "Operating Mode",
        value_range=(0, 16),
        units=None,
        default=3  # Position Control Mode
    ),
    "SECONDARY_ID": ControlTableItem(
        12, 1, AccessType.READ_WRITE,
        "Secondary ID",
        value_range=(0, 252),
        units=None,
        default=255
    ),
    "PROTOCOL_VERSION": ControlTableItem(
        13, 1, AccessType.READ_WRITE,
        "Protocol Version",
        value_range=(1, 2),
        units=None,
        default=2
    ),
    "HOMING_OFFSET": ControlTableItem(
        20, 4, AccessType.READ_WRITE,
        "Home Position Offset",
        value_range=(-1044479, 1044479),
        units="pulse",
        default=0
    ),
    "MOVING_THRESHOLD": ControlTableItem(
        24, 4, AccessType.READ_WRITE,
        "Velocity Threshold for Movement Detection",
        value_range=(0, 1023),
        units="0.229 rev/min",
        default=10
    ),
    "TEMPERATURE_LIMIT": ControlTableItem(
        31, 1, AccessType.READ_WRITE,
        "Maximum Internal Temperature Limit",
        value_range=(0, 100),
        units="°C",
        default=80
    ),
    "MAX_VOLTAGE_LIMIT": ControlTableItem(
        32, 2, AccessType.READ_WRITE,
        "Maximum Input Voltage Limit",
        value_range=(95, 160),
        units="0.1V",
        default=160
    ),
    "MIN_VOLTAGE_LIMIT": ControlTableItem(
        34, 2, AccessType.READ_WRITE,
        "Minimum Input Voltage Limit",
        value_range=(95, 160),
        units="0.1V",
        default=95
    ),
    "PWM_LIMIT": ControlTableItem(
        36, 2, AccessType.READ_WRITE,
        "Maximum PWM Limit",
        value_range=(0, 885),
        units=None,
        default=885
    ),
    "VELOCITY_LIMIT": ControlTableItem(
        44, 4, AccessType.READ_WRITE,
        "Maximum Velocity Limit",
        value_range=(0, 1023),
        units="0.229 rev/min",
        default=1023
    ),
    "MAX_POSITION_LIMIT": ControlTableItem(
        48, 4, AccessType.READ_WRITE,
        "Maximum Position Limit",
        value_range=(0, 4095),
        units="pulse",
        default=4095
    ),
    "MIN_POSITION_LIMIT": ControlTableItem(
        52, 4, AccessType.READ_WRITE,
        "Minimum Position Limit",
        value_range=(0, 4095),
        units="pulse",
        default=0
    ),
    "SHUTDOWN": ControlTableItem(
        63, 1, AccessType.READ_WRITE,
        "Shutdown Error Information",
        value_range=(0, 127),
        units=None,
        default=52
    ),
}

# RAM Area (Reset after power cycle)
RAM_REGISTERS = {
    "TORQUE_ENABLE": ControlTableItem(
        64, 1, AccessType.READ_WRITE,
        "Motor Torque On/Off",
        value_range=(0, 1),
        units=None,
        default=0
    ),
    "LED": ControlTableItem(
        65, 1, AccessType.READ_WRITE,
        "Status LED On/Off",
        value_range=(0, 1),
        units=None,
        default=0
    ),
    "STATUS_RETURN_LEVEL": ControlTableItem(
        68, 1, AccessType.READ_WRITE,
        "Status Return Level",
        value_range=(0, 2),
        units=None,
        default=2
    ),
    "REGISTERED_INSTRUCTION": ControlTableItem(
        69, 1, AccessType.READ_ONLY,
        "Registered Instruction Status",
        value_range=(0, 1),
        units=None,
        default=0
    ),
    "HARDWARE_ERROR_STATUS": ControlTableItem(
        70, 1, AccessType.READ_ONLY,
        "Hardware Error Status",
        value_range=None,
        units=None,
        default=0
    ),
    "VELOCITY_I_GAIN": ControlTableItem(
        76, 2, AccessType.READ_WRITE,
        "Velocity I Gain",
        value_range=(0, 16383),
        units=None,
        default=1000
    ),
    "VELOCITY_P_GAIN": ControlTableItem(
        78, 2, AccessType.READ_WRITE,
        "Velocity P Gain",
        value_range=(0, 16383),
        units=None,
        default=100
    ),
    "POSITION_D_GAIN": ControlTableItem(
        80, 2, AccessType.READ_WRITE,
        "Position D Gain",
        value_range=(0, 16383),
        units=None,
        default=2000
    ),
    "POSITION_I_GAIN": ControlTableItem(
        82, 2, AccessType.READ_WRITE,
        "Position I Gain",
        value_range=(0, 16383),
        units=None,
        default=0
    ),
    "POSITION_P_GAIN": ControlTableItem(
        84, 2, AccessType.READ_WRITE,
        "Position P Gain",
        value_range=(0, 16383),
        units=None,
        default=640
    ),
    "FEEDFORWARD_2ND_GAIN": ControlTableItem(
        88, 2, AccessType.READ_WRITE,
        "Feedforward 2nd Gain",
        value_range=(0, 16383),
        units=None,
        default=0
    ),
    "FEEDFORWARD_1ST_GAIN": ControlTableItem(
        90, 2, AccessType.READ_WRITE,
        "Feedforward 1st Gain",
        value_range=(0, 16383),
        units=None,
        default=0
    ),
    "BUS_WATCHDOG": ControlTableItem(
        98, 1, AccessType.READ_WRITE,
        "Bus Watchdog",
        value_range=(1, 127),
        units="20 msec",
        default=0
    ),
    "GOAL_PWM": ControlTableItem(
        100, 2, AccessType.READ_WRITE,
        "Target PWM Value",
        value_range=(-PWM_LIMIT, PWM_LIMIT),
        units=None,
        default=0
    ),
    "GOAL_VELOCITY": ControlTableItem(
        104, 4, AccessType.READ_WRITE,
        "Target Velocity Value",
        value_range=(-VELOCITY_LIMIT, VELOCITY_LIMIT),
        units="0.229 rev/min",
        default=0
    ),
    "PROFILE_ACCELERATION": ControlTableItem(
        108, 4, AccessType.READ_WRITE,
        "Acceleration Value of Profile",
        value_range=(0, 32767),
        units="214.577 rev/min²",
        default=0
    ),
    "PROFILE_VELOCITY": ControlTableItem(
        112, 4, AccessType.READ_WRITE,
        "Velocity Value of Profile",
        value_range=(0, 32767),
        units="0.229 rev/min",
        default=0
    ),
    "GOAL_POSITION": ControlTableItem(
        116, 4, AccessType.READ_WRITE,
        "Target Position Value",
        value_range=(MIN_POSITION_LIMIT, MAX_POSITION_LIMIT),
        units="pulse",
        default=None
    ),
    "REALTIME_TICK": ControlTableItem(
        120, 2, AccessType.READ_ONLY,
        "Real Time Clock",
        value_range=(0, 32767),
        units="1 msec",
        default=None
    ),
    "MOVING": ControlTableItem(
        122, 1, AccessType.READ_ONLY,
        "Movement Status",
        value_range=(0, 1),
        units=None,
        default=0
    ),
    "MOVING_STATUS": ControlTableItem(
        123, 1, AccessType.READ_ONLY,
        "Detailed Movement Status",
        value_range=(0, 255),
        units=None,
        default=0
    ),
    "PRESENT_PWM": ControlTableItem(
        124, 2, AccessType.READ_ONLY,
        "Present PWM Value",
        value_range=None,
        units=None,
        default=None
    ),
    "PRESENT_LOAD": ControlTableItem(
        126, 2, AccessType.READ_ONLY,
        "Present Load Value",
        value_range=None,
        units="%",
        default=None
    ),
    "PRESENT_VELOCITY": ControlTableItem(
        128, 4, AccessType.READ_ONLY,
        "Present Velocity Value",
        value_range=None,
        units="0.229 rev/min",
        default=None
    ),
    "PRESENT_POSITION": ControlTableItem(
        132, 4, AccessType.READ_ONLY,
        "Present Position Value",
        value_range=None,
        units="pulse",
        default=None
    ),
    "VELOCITY_TRAJECTORY": ControlTableItem(
        136, 4, AccessType.READ_ONLY,
        "Velocity Profile Value",
        value_range=None,
        units="0.229 rev/min",
        default=None
    ),
    "POSITION_TRAJECTORY": ControlTableItem(
        140, 4, AccessType.READ_ONLY,
        "Position Profile Value",
        value_range=None,
        units="pulse",
        default=None
    ),
    "PRESENT_INPUT_VOLTAGE": ControlTableItem(
        144, 2, AccessType.READ_ONLY,
        "Present Input Voltage",
        value_range=None,
        units="0.1V",
        default=None
    ),
    "PRESENT_TEMPERATURE": ControlTableItem(
        146, 1, AccessType.READ_ONLY,
        "Present Internal Temperature",
        value_range=None,
        units="°C",
        default=None
    ),
}

# Combine all registers
CONTROL_TABLE = {**EEPROM_REGISTERS, **RAM_REGISTERS}

class XM430W210Model(DynamixelModel):
    """
    XM430-W210 model definition.
    
    Features:
    - Position Control Mode
    - Velocity Control Mode
    - Current Control Mode
    - Extended Position Control Mode
    - PWM Control Mode
    
    Specifications:
    - Resolution: 4096 [pulse/rev]
    - Operating Voltage: 11.0-14.8V
    - Max Position: 360 degrees
    - Max Velocity: 41 rpm @ 12V
    """
    
    MODEL_NUMBER = 1030
    PROTOCOL_VERSION = PROTOCOL_2
    
    def __init__(self):
        super().__init__()
        self.control_table = CONTROL_TABLE
        self.features = {
            "position_control",
            "velocity_control",
            "current_control",
            "extended_position",
            "pwm_control"
        }
        
    def position_to_degrees(self, position: int) -> float:
        """
        Convert position value to degrees.
        
        Args:
            position: Raw position value (0-4095)
            
        Returns:
            float: Position in degrees (0-360)
        """
        return (position * 360.0) / 4096.0
        
    def degrees_to_position(self, degrees: float) -> int:
        """
        Convert degrees to position value.
        
        Args:
            degrees: Position in degrees (0-360)
            
        Returns:
            int: Raw position value (0-4095)
        """
        return int((degrees * 4096.0) / 360.0)
        
    def velocity_to_rpm(self, velocity: int) -> float:
        """
        Convert velocity value to RPM.
        
        Args:
            velocity: Raw velocity value
            
        Returns:
            float: Velocity in RPM
            
        Note:
            Velocity of 0 represents maximum RPM in CCW direction
            Velocity of 1023 represents maximum RPM in CW direction
        """
        return velocity * 0.229
        
    def rpm_to_velocity(self, rpm: float) -> int:
        """
        Convert RPM to velocity value.
        
        Args:
            rpm: Velocity in RPM
            
        Returns:
            int: Raw velocity value
            
        Note:
            Maximum RPM depends on operating voltage
            41 RPM at 12V
        """
        return int(rpm / 0.229) 