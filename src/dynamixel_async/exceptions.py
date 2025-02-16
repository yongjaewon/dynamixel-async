"""Exception classes for Dynamixel-Async library."""

from typing import Optional


class DynamixelError(Exception):
    """Base exception for all Dynamixel-related errors."""
    pass


class DynamixelConnectionError(DynamixelError):
    """Raised when there are issues with the serial connection."""
    
    def __init__(self, message: str, port: Optional[str] = None):
        self.port = port
        super().__init__(f"{message} (port: {port})" if port else message)


class DynamixelTimeoutError(DynamixelError):
    """Raised when a command times out."""
    
    def __init__(self, message: str, timeout: Optional[float] = None):
        self.timeout = timeout
        super().__init__(
            f"{message} (timeout: {timeout}s)" if timeout else message
        )


class DynamixelServoError(DynamixelError):
    """Raised when there's an error with a specific servo."""
    
    def __init__(self, message: str, servo_id: Optional[int] = None):
        self.servo_id = servo_id
        super().__init__(
            f"{message} (servo ID: {servo_id})" if servo_id else message
        )


class DynamixelModelError(DynamixelError):
    """Raised when there's an error with servo model detection or configuration."""
    
    def __init__(
        self, 
        message: str, 
        model_number: Optional[int] = None,
        servo_id: Optional[int] = None
    ):
        self.model_number = model_number
        self.servo_id = servo_id
        msg = message
        if model_number:
            msg = f"{msg} (model: {model_number})"
        if servo_id:
            msg = f"{msg} (servo ID: {servo_id})"
        super().__init__(msg)


class DynamixelProtocolError(DynamixelError):
    """Raised when there's a protocol-level error."""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[int] = None,
        instruction: Optional[int] = None
    ):
        self.error_code = error_code
        self.instruction = instruction
        msg = message
        if error_code is not None:
            msg = f"{msg} (error code: 0x{error_code:02x})"
        if instruction is not None:
            msg = f"{msg} (instruction: 0x{instruction:02x})"
        super().__init__(msg)


class DynamixelChecksumError(DynamixelProtocolError):
    """Raised when packet checksum validation fails."""
    pass


class DynamixelHardwareError(DynamixelError):
    """Raised when servo reports a hardware error."""
    
    def __init__(
        self,
        message: str,
        error_bits: Optional[int] = None,
        servo_id: Optional[int] = None
    ):
        self.error_bits = error_bits
        self.servo_id = servo_id
        msg = message
        if error_bits is not None:
            msg = f"{msg} (error bits: 0x{error_bits:02x})"
        if servo_id is not None:
            msg = f"{msg} (servo ID: {servo_id})"
        super().__init__(msg) 