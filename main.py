import threading
import logging
import logging.config
import yaml
import time
from pyfirmata import Arduino, util
from sen0386 import Sen0386
from lm298 import MotorControl

"""
Constants
"""
LOGGER = "main"
SEN0386_SERIALNO = "AB0O5A7Z"
MOTORCONTROL_E1 = "d:6:o"
MOTORCONTROL_PWM1 = "d:5:p"
MOTORCONTROL_PWM2 = "d:3:p"
MOTORCONTROL_E2 = "d:4:o"
ARDUINO_DEVICE = "/dev/ttyACM0"
"""
Current sensor values
"""
sen038SensorValues = None

"""
Setup logging    
"""
with open(file = 'logging.yaml', mode = 'r') as stream:
    config = yaml.load(stream = stream, Loader = yaml.FullLoader)
    logging.config.dictConfig(config)

logger = logging.getLogger(LOGGER)
logger.info("Logging setup")
"""
Setting up modules
"""
logger.info("Starting setup")
sen0386 = Sen0386(serialno = SEN0386_SERIALNO)
logger.info("Sen0386 setup")

"""
Setting up gpio
"""
logger.info("Starting setup gpio")
board = Arduino(ARDUINO_DEVICE)
e1Pin = board.get_pin(MOTORCONTROL_E1)
pwm1Pin = board.get_pin(MOTORCONTROL_PWM1)
pwm2Pin = board.get_pin(MOTORCONTROL_PWM2)
e2Pin = board.get_pin(MOTORCONTROL_E2)
logger.info("Finished setup gpio")

"""
Setting up motorcontrol
"""
motorControl = MotorControl(MOTORCONTROL_E1, MOTORCONTROL_PWM1, MOTORCONTROL_PWM2, MOTORCONTROL_E2)

"""
Thread module setup
"""
def sen038Thread():
    logger.info("Starting sen038Thread")  
    while True:
        sen038SensorValues = sen0386.readSensorValues()
        print(sen038SensorValues)

logger.info("Starting thread setup")        
sen0386Thread = threading.Thread(target = sen038Thread)
sen0386Thread.start()
logger.info("Completed Sen0386 setup")

time.sleep(1)
motorControl.disableMotors()
time.sleep(1)
motorControl.enableMotors()
time.sleep(1)
motorControl.forward(speed = 75, direction = MotorControl.DIRECTION_FORWARD)
time.sleep(1)
motorControl.stop()