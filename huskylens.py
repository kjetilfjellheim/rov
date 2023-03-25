import serial
import serial.tools.list_ports as ports
import time

COMMAND_PRE = "55AA11"
COMMAND_PING = "002c3c"
COMMAND_FORGET = "003747"
COMMAND_LEARNED = "002333"
COMMAND_ALGORITHM_OBJECT_TRACKING = "022d0100"
COMMAND_ALGORITHM_FACE_RECOGNITION = "022d0000"
COMMAND_ALGORITHM_OBJECT_RECOGNITION = "022d0200"
COMMAND_ALGORITHM_LINE_TRACKING = "022d0300"
COMMAND_ALGORITHM_COLOR_RECOGNITION = "022d0400"
COMMAND_ALGORITHM_TAG_RECOGNITION = "022d0500"
COMMAND_ALGORITHM_OBJECT_CLASSIFICATION = "022d0600"
COMMAND_ALGORITHM_QR_CODE_RECOGNTITION = "022d0700"
COMMAND_ALGORITHM_BARCODE_RECOGNTITION = "022d0800"
COMMAND_SCREESNSHOT = "003949"
COMMAND_SAVE_PICTURE = "003040"
COMMAND_SAVE_MODEL = "0232"
COMMAND_ARROWS_BY_ID = "0228"
COMMAND_LEARN = ""

INITIAL_READ_SIZE = 5
HEADER_START = 0
HEADER_STOP = 4
ADDRESS_START = 4
ADDRESS_STOP = 6
DATA_LENGTH_START = 6
DATA_LENGTH_STOP = 8
BASE16 = 16
COMMAND_START = 8
COMMAND_STOP = 10
DATA_START = 10

class Response:
    def __init__(self, success, headers = None, address = None, command = None, data = None, checksum = None, numberOfElements = None):
        self.success = success
        self.headers = headers
        self.address = address
        self.command = command
        self.data = data
        self.checksum = checksum
        self.numberOfElements = numberOfElements
        
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
        cmd = self.generateCommand(command, id)
        self.writeCommand(cmd)
        return self.handleResponse()

    def handleResponse(self):
        byteString = self.port.read(INITIAL_READ_SIZE)
        if (self.isResponseReceived(byteString)):
            byteString += self.port.read(int(byteString[3]) + 1)
            responseData=byteString.hex()   
            if (responseData == None):
                return Response(False)
            else:
                headers = responseData[HEADER_START:HEADER_STOP]
                address = responseData[ADDRESS_START:ADDRESS_STOP]
                command = responseData[COMMAND_START:COMMAND_STOP]
                data_length = int(responseData[DATA_LENGTH_START:DATA_LENGTH_STOP], BASE16)
                data = []
                numberOfElements = None
                if(data_length > 0):
                    data = responseData[DATA_START:DATA_START+data_length*2]  
                    numberOfElements = int(data[2:4]+data[0:2], BASE16)                    
                checksum = responseData[2*(6+data_length-1):2*(6+data_length-1)+2]                         
                return Response(True, headers = headers, address = address, command = command, data = data, checksum = checksum, numberOfElements = numberOfElements)
        return Response(False)

    def generateCommand(self, command, id):
        cmd = COMMAND_PRE + command;
        if id != None:
            data = "{:04x}".format(id)
            part1=data[2:]
            part2=data[0:2]
            data=part1+part2
            dataLen = "{:02x}".format(len(data)//2)
            cmd = cmd + dataLen + "36" + data
        cmd += self.calculateChecksum(cmd)
        return cmd
    
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

