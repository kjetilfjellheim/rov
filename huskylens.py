import serial
import serial.tools.list_ports as ports
import time

COMMAND_PRE = "55AA11"
COMMAND_PING = "002c3c"
COMMAND_FORGET = "003747"
COMMAND_LEARNED = "002333"
COMMAND_ALGORITM_COLOR_RECOGNITION = "022d0400"
COMMAND_LEARN = ""

INITIAL_READ_SIZE = 5
HEADER_START = 0
HEADER_STOP = 4
ADDRESS_START = 4
ADDRESS_STOP = 6
DATA_LENGTH_START = 6
DATA_LENGTH_STOP = 8
DATA_LENGTH_BASE = 16
COMMAND_START = 8
COMMAND_STOP = 10
DATA_START = 10

class Response:

    headers = None
    address = None
    command = None
    data = None
    checkSum = None

    def __init__(self, responseData = None):
        if (responseData == None):
            self.success = False
        else:
            self.success = True
            self.headers = responseData[HEADER_START:HEADER_STOP]
            self.address = responseData[ADDRESS_START:ADDRESS_STOP]
            self.command = responseData[COMMAND_START:COMMAND_STOP]
            data_length = int(responseData[DATA_LENGTH_START:DATA_LENGTH_STOP], DATA_LENGTH_BASE)
            if(data_length > 0):
                self.data = responseData[DATA_START:DATA_START+data_length*2]
            else:
                self.data = []
            self.checkSum = responseData[2*(6+data_length-1):2*(6+data_length-1)+2]

    def pingSuccess(self):
        return "2e" == self.command

class Huskylens:
    
    def __init__(self, vid=None, pid=None, serialno=None):
        usb_port = self.findUsbPort(vid, pid, serialno)
        self.port = serial.Serial(
                        port=usb_port.device,
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=.5)
        self.port.dtr = False
        self.port.rts = False
            
    def findUsbPort(self, vid, pid, serialno):
        com_ports = list(ports.comports())
        for port in com_ports:
            if  (vid == None or port.vid == vid) and (pid == None or port.pid == pid) and (serialno == None or port.serial_number == serialno):
                return port
        return None
    
    def isResponseReceived(self, initialResponse):
        return (len(initialResponse) == INITIAL_READ_SIZE)
    
    def command(self, command, id=None):
        cmd = COMMAND_PRE + command;
        if id != None:
            data = "{:04x}".format(id)
            part1=data[2:]
            part2=data[0:2]
            data=part1+part2
            dataLen = "{:02x}".format(len(data)//2)
            cmd = cmd + dataLen + "36" + data
        cmd += self.calculateChecksum(cmd)
        self.writeCommand(cmd)
        byteString = self.port.read(INITIAL_READ_SIZE)
        if (self.isResponseReceived(byteString)):
            byteString += self.port.read(int(byteString[3]) + 1)
            return Response(responseData=byteString.hex())
        return Response()
    
    def writeCommand(self, cmd):
        self.port.flushInput()
        self.port.flush()
        data = bytes.fromhex(cmd)
        self.port.write(data)
        
    def calculateChecksum(self, hexStr):
        total = 0
        for i in range(0, len(hexStr), 2):
            total += int(hexStr[i:i+2], 16)
        hexStr = hex(total)[-2:]
        return hexStr        


