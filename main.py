import threading
import logging
import logging.config
import yaml
from pyfirmata import Arduino
from sen0386 import Sen0386
from lm298 import MotorControl

"""
Constants
"""
LOGGER = "main"                 #Logger name
SEN0386_SERIALNO = "AB0O5A7Z"   #Serial no of th ftdi interface device
MOTORCONTROL_PWM1 = "d:6:p"     #Digital pin 6 pwm output
MOTORCONTROL_M1 = "d:5:o"       #Digital pin 5 output
MOTORCONTROL_M2 = "d:4:o"       #Digital pin 4 output
MOTORCONTROL_PWM2 = "d:3:p"     #Digital pin 3 pwm output
ARDUINO_DEVICE = "/dev/ttyACM0" #Arduino device on Lattepanda
"""
Current sensor values
"""
sen038SensorValues = None       #Latest sen0386 sensor values read

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
pwm1Pin = board.get_pin(MOTORCONTROL_PWM1)
m1Pin = board.get_pin(MOTORCONTROL_M1)
m2Pin = board.get_pin(MOTORCONTROL_M2)
pwm2Pin = board.get_pin(MOTORCONTROL_PWM2)
logger.info("Finished setup gpio")

"""
Setting up motorcontrol
"""
motorControl = MotorControl(pwm1Pin, m1Pin, m2Pin, pwm2Pin)

"""
Thread module setup
"""
def sen038Thread():
    logger.info("Starting sen038Thread")  
    while True:
        sen038SensorValues = sen0386.readSensorValues()

logger.info("Starting thread setup")        
sen0386Thread = threading.Thread(target = sen038Thread)
sen0386Thread.start()
logger.info("Completed Sen0386 setup")

"""Just demo"""
#motorControl.forward(speed = 100, direction = MotorControl.DIRECTION_FORWARD)			--No movement
#motorControl.forward(speed = 100, direction = MotorControl.DIRECTION_BACK)			    --OK
#motorControl.rotateInPlace(speed = 100, direction = MotorControl.DIRECTION_LEFT)		--OK
#motorControl.rotateInPlace(speed = 100, direction = MotorControl.DIRECTION_RIGHT)		--No movement
#motorControl.turnDifferential(100,0, MotorControl.DIRECTION_FORWARD)					--No movement
#motorControl.turnDifferential(0,100, MotorControl.DIRECTION_FORWARD)					--No movement
#motorControl.turnDifferential(100,0, MotorControl.DIRECTION_BACK)						--OK
#motorControl.turnDifferential(0,100, MotorControl.DIRECTION_BACK)						--OK, except left stil slightly move
#motorControl.stop()																	--OK
