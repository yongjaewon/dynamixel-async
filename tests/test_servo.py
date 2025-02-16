import pytest
from unittest.mock import Mock, patch
from dynamixel_async import (
    DynamixelServo, DynamixelError, DynamixelModelError,
    XM430W210, OperatingMode
)

@pytest.fixture
def mock_port_handler():
    return Mock()

@pytest.fixture
def mock_packet_handler():
    handler = Mock()
    handler.getTxRxResult.return_value = "Success"
    handler.getRxPacketError.return_value = 0
    return handler

@pytest.fixture
def servo(mock_port_handler, mock_packet_handler):
    servo = DynamixelServo(mock_port_handler, mock_packet_handler, servo_id=1)
    servo.model = XM430W210()
    return servo

def test_servo_initialization(servo):
    assert servo.id == 1
    assert isinstance(servo.model, XM430W210)

def test_enable_torque(servo, mock_packet_handler):
    mock_packet_handler.write1ByteTxRx.return_value = (0, 0)  # Success
    assert servo.enable_torque()
    mock_packet_handler.write1ByteTxRx.assert_called_once()

def test_set_position(servo, mock_packet_handler):
    mock_packet_handler.write4ByteTxRx.return_value = (0, 0)  # Success
    assert servo.set_position(180.0)
    mock_packet_handler.write4ByteTxRx.assert_called_once()

def test_get_position(servo, mock_packet_handler):
    mock_packet_handler.read4ByteTxRx.return_value = (0, 2048, 0)  # Success, mid position
    assert servo.get_position() == 180.0
    mock_packet_handler.read4ByteTxRx.assert_called_once()

def test_set_operating_mode(servo, mock_packet_handler):
    mock_packet_handler.write1ByteTxRx.return_value = (0, 0)  # Success
    assert servo.set_operating_mode(OperatingMode.POSITION)
    mock_packet_handler.write1ByteTxRx.assert_called_once()

def test_error_handling(servo, mock_packet_handler):
    mock_packet_handler.write1ByteTxRx.return_value = (1, 0)  # Communication error
    with pytest.raises(DynamixelError):
        servo.enable_torque()

def test_no_model_error(mock_port_handler, mock_packet_handler):
    servo = DynamixelServo(mock_port_handler, mock_packet_handler, servo_id=1)
    with pytest.raises(DynamixelModelError):
        servo.enable_torque() 