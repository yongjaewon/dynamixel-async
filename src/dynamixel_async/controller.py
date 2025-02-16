"""High-level controller for multiple Dynamixel servos."""

import logging
import asyncio
from typing import Dict, List, Optional, Set
import serial.tools.list_ports
from dynamixel_sdk.port_handler import PortHandler
from dynamixel_sdk.packet_handler import PacketHandler
from .servo import DynamixelServo
from .constants import Baudrate
from .exceptions import DynamixelConnectionError, DynamixelTimeoutError

logger = logging.getLogger(__name__)

def find_dynamixel_port() -> Optional[str]:
    """
    Find the most likely port for a Dynamixel controller.
    
    Returns:
        str: Port name if found, None otherwise
    """
    DYNAMIXEL_VENDORS = {
        "0403",  # FTDI
        "10c4",  # Silicon Labs
        "067b",  # Prolific
    }
    
    # First try to find a port with matching vendor ID
    for port in serial.tools.list_ports.comports():
        if hasattr(port, 'vid') and port.vid:
            vid = hex(port.vid)[2:].lower()
            if vid in DYNAMIXEL_VENDORS:
                logger.info(f"Found likely Dynamixel controller on {port.device}")
                return port.device
    
    # Fallback to first USB serial port
    for port in serial.tools.list_ports.comports():
        if "USB" in port.device:
            logger.info(f"Using fallback USB port {port.device}")
            return port.device
    
    return None

class DynamixelController:
    """
    High-level controller for multiple Dynamixel servos.
    
    Handles port management, servo discovery, and provides a high-level
    interface for controlling multiple servos.
    """
    
    def __init__(
        self,
        port: Optional[str] = None,
        baudrate: int = 57600,
        protocol_version: float = 2.0
    ):
        self.port = port
        self.baudrate = baudrate
        self.protocol_version = protocol_version
        self.port_handler = None
        self.packet_handler = None
        self.servos: Dict[int, DynamixelServo] = {}
        
    async def connect(self, scan_ids: Optional[List[int]] = None) -> bool:
        """
        Connect to the Dynamixel controller and scan for servos.
        
        Args:
            scan_ids: Optional list of servo IDs to scan. If None, scans common IDs.
            
        Returns:
            bool: True if connection successful
            
        Raises:
            DynamixelConnectionError: If connection fails
        """
        try:
            # Find port if not specified
            if not self.port:
                self.port = find_dynamixel_port()
            if not self.port:
                raise DynamixelConnectionError("No suitable port found")
                
            # Initialize port
            self.port_handler = PortHandler(self.port)
            if not self.port_handler.openPort():
                raise DynamixelConnectionError(f"Failed to open port {self.port}")
                
            # Set baudrate
            if not self.port_handler.setBaudRate(self.baudrate):
                raise DynamixelConnectionError(f"Failed to set baudrate to {self.baudrate}")
                
            # Initialize protocol
            self.packet_handler = PacketHandler(self.protocol_version)
            
            # Scan for servos
            if scan_ids is None:
                scan_ids = list(range(1, 5))  # Default to scanning IDs 1-4
                
            await self.scan_servos(scan_ids)
            
            logger.info(f"Successfully connected to {len(self.servos)} servos")
            return True
            
        except Exception as e:
            raise DynamixelConnectionError(f"Failed to connect: {str(e)}")
            
    async def disconnect(self) -> None:
        """Disconnect from the controller and clean up."""
        if self.port_handler:
            self.port_handler.closePort()
            self.port_handler = None
        self.packet_handler = None
        self.servos.clear()
        logger.info("Disconnected from Dynamixel controller")
        
    async def scan_servos(self, ids: List[int]) -> Set[int]:
        """
        Scan for servos with the specified IDs.
        
        Args:
            ids: List of IDs to scan for
            
        Returns:
            Set of found servo IDs
            
        Raises:
            DynamixelConnectionError: If not connected
        """
        if not self.port_handler or not self.packet_handler:
            raise DynamixelConnectionError("Not connected")
            
        found_ids = set()
        for servo_id in ids:
            try:
                model = await DynamixelServo.detect_model(
                    self.port_handler,
                    self.packet_handler,
                    servo_id
                )
                if model:
                    servo = DynamixelServo(
                        self.port_handler,
                        self.packet_handler,
                        servo_id,
                        model
                    )
                    self.servos[servo_id] = servo
                    found_ids.add(servo_id)
                    logger.info(f"Found {model.name} at ID {servo_id}")
            except Exception as e:
                logger.debug(f"No servo found at ID {servo_id}: {e}")
                
        return found_ids
        
    def get_servo(self, servo_id: int) -> Optional[DynamixelServo]:
        """Get a servo by ID if it exists."""
        return self.servos.get(servo_id)
        
    async def set_all_torque(self, enable: bool) -> bool:
        """
        Enable or disable torque on all connected servos.
        
        Args:
            enable: True to enable, False to disable
            
        Returns:
            bool: True if all servos were successfully set
        """
        success = True
        for servo in self.servos.values():
            try:
                if enable:
                    if not servo.enable_torque():
                        success = False
                else:
                    if not servo.disable_torque():
                        success = False
            except Exception as e:
                logger.error(f"Error setting torque on servo {servo.id}: {e}")
                success = False
        return success
        
    async def wait_for_servos(self, timeout: float = 5.0) -> bool:
        """
        Wait for all servos to stop moving.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            bool: True if all servos stopped, False if timeout
            
        Raises:
            DynamixelTimeoutError: If timeout occurs
        """
        start_time = asyncio.get_event_loop().time()
        while True:
            all_stopped = True
            for servo in self.servos.values():
                try:
                    moving = servo._read_from_address("MOVING")
                    if moving:
                        all_stopped = False
                        break
                except Exception as e:
                    logger.error(f"Error checking servo {servo.id} movement: {e}")
                    all_stopped = False
                    
            if all_stopped:
                return True
                
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise DynamixelTimeoutError("Timeout waiting for servos to stop")
                
            await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
            
    def get_connected_ids(self) -> List[int]:
        """Get list of connected servo IDs."""
        return list(self.servos.keys()) 