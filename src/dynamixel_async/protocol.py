"""Protocol definitions for Dynamixel communication."""

from enum import IntEnum


class Instruction(IntEnum):
    """Dynamixel protocol instructions."""
    PING = 0x01
    READ = 0x02
    WRITE = 0x03
    REG_WRITE = 0x04
    ACTION = 0x05
    FACTORY_RESET = 0x06
    REBOOT = 0x08
    CLEAR = 0x10
    STATUS = 0x55
    SYNC_READ = 0x82
    SYNC_WRITE = 0x83
    BULK_READ = 0x92
    BULK_WRITE = 0x93


class PacketState(IntEnum):
    """States for packet parsing."""
    HEADER1 = 0
    HEADER2 = 1
    HEADER3 = 2
    RESERVED = 3
    ID = 4
    LENGTH_L = 5
    LENGTH_H = 6
    INSTRUCTION = 7
    ERROR = 8
    PARAMETER = 9
    CRC_L = 10
    CRC_H = 11


# Protocol 2.0 definitions
HEADER = [0xFF, 0xFF, 0xFD]
RESERVED = 0x00
MAX_PACKET_LENGTH = 256
MIN_PACKET_LENGTH = 10  # Header(3) + Reserved(1) + ID(1) + Length(2) + Instruction(1) + CRC(2)

# CRC lookup table for Protocol 2.0
CRC_TABLE = [
    0x0000, 0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
    0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027, 0x0022,
    0x8063, 0x0066, 0x006C, 0x8069, 0x0078, 0x807D, 0x8077, 0x0072,
    0x0050, 0x8055, 0x805F, 0x005A, 0x804B, 0x004E, 0x0044, 0x8041,
    0x80C3, 0x00C6, 0x00CC, 0x80C9, 0x00D8, 0x80DD, 0x80D7, 0x00D2,
    0x00F0, 0x80F5, 0x80FF, 0x00FA, 0x80EB, 0x00EE, 0x00E4, 0x80E1,
    0x00A0, 0x80A5, 0x80AF, 0x00AA, 0x80BB, 0x00BE, 0x00B4, 0x80B1,
    0x8093, 0x0096, 0x009C, 0x8099, 0x0088, 0x808D, 0x8087, 0x0082,
]


def update_crc(crc_accum: int, data_blk: bytes) -> int:
    """
    Calculate CRC for Protocol 2.0.
    
    Args:
        crc_accum: Initial CRC value
        data_blk: Data to calculate CRC for
        
    Returns:
        int: Updated CRC value
    """
    for data in data_blk:
        i = ((crc_accum >> 8) ^ data) & 0xFF
        crc_accum = ((crc_accum << 8) ^ CRC_TABLE[i]) & 0xFFFF
    return crc_accum


class ErrorBit(IntEnum):
    """Hardware error bits reported by servos."""
    NONE = 0x00
    INPUT_VOLTAGE = 0x01
    OVERHEATING = 0x02
    MOTOR_ENCODER = 0x04
    ELECTRICAL_SHOCK = 0x08
    OVERLOAD = 0x10
    
    @classmethod
    def decode(cls, error_byte: int) -> set:
        """Decode error byte into set of error conditions."""
        errors = set()
        if error_byte & cls.INPUT_VOLTAGE:
            errors.add("Input Voltage Error")
        if error_byte & cls.OVERHEATING:
            errors.add("Overheating Error")
        if error_byte & cls.MOTOR_ENCODER:
            errors.add("Motor Encoder Error")
        if error_byte & cls.ELECTRICAL_SHOCK:
            errors.add("Electrical Shock Error")
        if error_byte & cls.OVERLOAD:
            errors.add("Overload Error")
        return errors 