import struct
import serial
import serial.tools.list_ports as ports
import logging

"""
Logger setup
"""
logger = logging.getLogger("sen0386")
loggerHw = logging.getLogger("sen0386_hw")

"""
Class definitions
"""
class Acceleration:
    def __init__(self, ax, ay, az):
        self.ax = ax
        self.ay = ay
        self.az = az
    
    
class AngularVelocity:
    def __init__(self, wx, wy, wz):
        self.wx = wx
        self.wy = wy
        self.wz = wz
    
class Gyro:
    def __init__(self, roll, pitch, yaw):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

class Response:
    def __init__(self, acceleration, angularVelocity, gyro):
        self.acceleration = acceleration
        self.angularVelocity = angularVelocity
        self.gyro = gyro
    

class Sen0386:

    PACKET_HEADER = 0x55
    ACC_PACKET_HEADER = 0x51
    ANGVEL_PACKET_HEADER = 0x52
    ANG_PACKET = 0x53
    ACCPACKET_BUFFER_START = 0
    ACCPACKET_BUFFER_END = 10
    ANGVELPACKET_BUFFER_START = 11
    ANGVELPACKET_BUFFER_END = 21
    ANGPACKET_BUFFER_START = 22
    ANGPACKET_BUFFER_END = 32
    BUFFER_SIZE = 100
    DATA_SIZE = 44
    PACKET_LENGTH = 10
    BYTE_PACKET_HEADER = 0
    BYTE_PACKET_TYPE = 1
    BYTE_AXL_DATA_CONTENT = 2
    BYTE_AXH_DATA_CONTENT = 3
    BYTE_AYL_DATA_CONTENT = 4
    BYTE_AYH_DATA_CONTENT = 5
    BYTE_AZL_DATA_CONTENT = 6
    BYTE_AZH_DATA_CONTENT = 7
    BYTE_WXL_DATA_CONTENT = 2
    BYTE_WXH_DATA_CONTENT = 3
    BYTE_WYL_DATA_CONTENT = 4
    BYTE_WYH_DATA_CONTENT = 5
    BYTE_WZL_DATA_CONTENT = 6
    BYTE_WZH_DATA_CONTENT = 7
    BYTE_ROLLL_DATA_CONTENT = 2
    BYTE_ROLLH_DATA_CONTENT = 3
    BYTE_PITCHL_DATA_CONTENT = 4
    BYTE_PITCHH_DATA_CONTENT = 5
    BYTE_YAWL_DATA_CONTENT = 6
    BYTE_YAWH_DATA_CONTENT = 7
    MAX_16_BIT_INTEGER_SIZE = 32768.00
    GRAVITY_CONSTANT = 9.81
    CALCULATION_GRAVITY_CONSTANT = GRAVITY_CONSTANT * 16.00
    CALCULATION_ROTATION_CONSTANT = 2000.00
    CALCULATION_ANGLE_CONSTANT = 180.00

    def __init__(self, vid=None, pid=None, serialno=None):
        usb_port = self.findUsbPort(vid, pid, serialno)
        self.port = serial.Serial(
                        port=usb_port.device,
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=1)
        self.port.dtr = False
        self.port.rts = False
            
    def findUsbPort(self, vid, pid, serialno):
        com_ports = list(ports.comports())
        for port in com_ports:
            if  (vid == None or port.vid == vid) and (pid == None or port.pid == pid) and (serialno == None or port.serial_number == serialno):
                return port
        return None

    def convertShort(self, packet, highByte, lowByte):
        b = bytearray(2)
        b[0] = packet[highByte]
        b[1] = packet[lowByte]
        result = struct.unpack(">h", b)[0]
        return result

    def handleAccPacket(self, accPacketData):
        if len(accPacketData) == self.PACKET_LENGTH and accPacketData[self.BYTE_PACKET_HEADER] is self.PACKET_HEADER and accPacketData[self.BYTE_PACKET_TYPE] is self.ACC_PACKET_HEADER:
            ax = (self.CALCULATION_GRAVITY_CONSTANT / self.MAX_16_BIT_INTEGER_SIZE) * self.convertShort(accPacketData, self.BYTE_AXH_DATA_CONTENT, self.BYTE_AXL_DATA_CONTENT)
            ay = (self.CALCULATION_GRAVITY_CONSTANT / self.MAX_16_BIT_INTEGER_SIZE) * self.convertShort(accPacketData, self.BYTE_AYH_DATA_CONTENT, self.BYTE_AYL_DATA_CONTENT)
            az = (self.CALCULATION_GRAVITY_CONSTANT / self.MAX_16_BIT_INTEGER_SIZE) * self.convertShort(accPacketData, self.BYTE_AZH_DATA_CONTENT, self.BYTE_AZL_DATA_CONTENT)
            return Acceleration(ax, ay, az)
        else:
            return Acceleration(None, None, None)

    def handleAngVelPacket(self, angVelPacketData):
        if len(angVelPacketData) == self.PACKET_LENGTH and angVelPacketData[self.BYTE_PACKET_HEADER] is self.PACKET_HEADER and angVelPacketData[self.BYTE_PACKET_TYPE] is self.ANGVEL_PACKET_HEADER:
            wx = (self.CALCULATION_ROTATION_CONSTANT / self.MAX_16_BIT_INTEGER_SIZE) * self.convertShort(angVelPacketData, self.BYTE_WXH_DATA_CONTENT, self.BYTE_WXL_DATA_CONTENT)
            wy = (self.CALCULATION_ROTATION_CONSTANT / self.MAX_16_BIT_INTEGER_SIZE) * self.convertShort(angVelPacketData, self.BYTE_WYH_DATA_CONTENT, self.BYTE_WYL_DATA_CONTENT)
            wz = (self.CALCULATION_ROTATION_CONSTANT / self.MAX_16_BIT_INTEGER_SIZE) * self.convertShort(angVelPacketData, self.BYTE_WZH_DATA_CONTENT, self.BYTE_WZL_DATA_CONTENT)
            return AngularVelocity(wx, wy, wz)
        else:
            return AngularVelocity(None, None, None)

    def handleAngPacket(self, angPacketData):
        if len(angPacketData) == self.PACKET_LENGTH and angPacketData[self.BYTE_PACKET_HEADER] is self.PACKET_HEADER and angPacketData[self.BYTE_PACKET_TYPE] is self.ANG_PACKET:
            roll = (self.CALCULATION_ANGLE_CONSTANT / self.MAX_16_BIT_INTEGER_SIZE) * self.convertShort(angPacketData, self.BYTE_ROLLH_DATA_CONTENT, self.BYTE_ROLLL_DATA_CONTENT)
            pitch = (self.CALCULATION_ANGLE_CONSTANT / self.MAX_16_BIT_INTEGER_SIZE) * self.convertShort(angPacketData, self.BYTE_PITCHH_DATA_CONTENT, self.BYTE_PITCHL_DATA_CONTENT)
            yaw = (self.CALCULATION_ANGLE_CONSTANT / self.MAX_16_BIT_INTEGER_SIZE) * self.convertShort(angPacketData, self.BYTE_YAWH_DATA_CONTENT, self.BYTE_YAWL_DATA_CONTENT)
            return Gyro(roll, pitch, yaw)
        else:
            return Gyro(None, None, None)

    def handlePackets(self, accPacketData, angVelPacketData, angPacketData):
        acceleration = self.handleAccPacket(accPacketData)
        angularVelocity = self.handleAngVelPacket(angVelPacketData)
        gyro = self.handleAngPacket(angPacketData)
        return Response(acceleration, angularVelocity, gyro)
    
    def findStartIndex(self, data):
        for index in range(self.BUFFER_SIZE):
            if data[index] == self.PACKET_HEADER and data[index+1] == self.ACC_PACKET_HEADER:
                return index
        return None

    def readSensorValues(self):
        self.port.flush()
        data = self.port.read(self.BUFFER_SIZE)
        if data is not None and len(data) == self.BUFFER_SIZE:
            first = self.findStartIndex(data)
            if (first != None):
                data = data[first:first+self.DATA_SIZE]
                loggerHw.info(data)
                accPacket = data[self.ACCPACKET_BUFFER_START:self.ACCPACKET_BUFFER_END]
                angVelPacket = data[self.ANGVELPACKET_BUFFER_START:self.ANGVELPACKET_BUFFER_END]
                angPacket = data[self.ANGPACKET_BUFFER_START:self.ANGPACKET_BUFFER_END]
                response = self.handlePackets(accPacket, angVelPacket, angPacket)
                logger.info("Sensor values read ax={0},ay={1},az={2},wx={3},wy={4},wz={5},roll={6},pitch={7},yaw={8}".format(response.acceleration.ax, response.acceleration.ay, response.acceleration.az, response.angularVelocity.wx, response.angularVelocity.wy, response.angularVelocity.wz, response.gyro.roll, response.gyro.pitch, response.gyro.yaw))
                return response
            else:
                logger.info("No sensor values read")
                return Response(None, None, None)
        else:
            logger.info("No sensor values read")
            return Response(None, None, None)