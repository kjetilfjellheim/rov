import logging

"""
Constants
"""
LOGGER = "lm298"
"""
Logger setup
"""
logger = logging.getLogger("lm298")

"""
Class definitions
"""
class MotorControl:
    """
    Constants
    """
    DIRECTION_LEFT = 1
    DIRECTION_RIGHT = -1
    DIRECTION_FORWARD = 1
    DIRECTION_BACK = -1
    STOP_DUTY_CYCLE = 50
    ON = 1
    OFF = 0

    """
    Class variables
    """
    e1Pin = None    #Enable pin for motor 1
    m1Pin = None    #Pwm pin for motor 1
    e2Pin = None    #Enable pin for motor 2
    m2Pin = None    #Pwm pin for motor 2

    def __init__(self, e1Pin, m1Pin, m2Pin, e2Pin):
        logger.info("Starting initalizing LM298")
        self.e1Pin = e1Pin
        self.m1Pin = m1Pin
        self.m2Pin = m2Pin
        self.e2Pin = e2Pin
        self.stop()
        logger.info("Finished initalizing LM298")

    """
    Enable motors by enabling pins by setting them to HIGH.
    """
    def enableMotors(self):
        self.e1Pin.write(self.ON)
        self.e2Pin.write(self.ON)
        logger.info("Enabled motors LM298")

    """
    Disable motors by disabling pins by setting them to LOW.
    """
    def disableMotors(self):
        self.e1Pin.write(self.OFF)
        self.e2Pin.write(self.OFF)
        logger.info("Disabled motors LM298")

    """
    Setting pwm value on motor. The value is a fraction between 0-1.
    """        
    def setPwm(self, pwm, value):
        writeVal = value / 100.0
        pwm.write(writeVal)
        if pwm == self.m1Pin:
            logger.info("PWM motor 1 written value {0} dutycycle set {1}".format(writeVal, value))
        elif pwm == self.m2Pin:
            logger.info("PWM motor 2 written value {0} dutycycle set {1}".format(writeVal, value))
        if pwm == self.m1Pin and value == 0:
            self.e1Pin.write(self.OFF)
        elif pwm == self.m1Pin and value > 0:
            self.e1Pin.write(self.ON)     
        elif pwm == self.m2Pin and value == 0:
            self.e2Pin.write(self.OFF)
        elif pwm == self.m2Pin and value > 0:
            self.e2Pin.write(self.ON)                 

    """
    Rotate in place by setting one motor forward and he other back at the same speed.
    """  
    def rotateInPlace(self, speed, direction):
        logger.info("Motors rotate in place")
        self.setPwm(self.m1Pin, 100 - (50 - (speed * direction / 2)))
        self.setPwm(self.m2Pin, 100 - (50 - (speed * direction / 2)))

    """
    Turn by setting left and right motors at different speed.
    """  
    def turnDifferential(self, speedLeft, speedRight, direction):
        logger.info("Motors turn differential")
        self.setPwm(self.m1Pin, 100 - (50 + (speedLeft * direction / 2)))
        self.setPwm(self.m2Pin, 100 - (50 - (speedRight * direction / 2)))

    """
    Move forward or back
    """  
    def forward(self, speed, direction):
        logger.info("Motors forward/reverse")
        self.setPwm(self.m1Pin, 100 - (50 + (speed * direction / 2)))
        self.setPwm(self.m2Pin, 100 - (50 - (speed * direction / 2)))
    
    """
    Stop both motors by disbaling enable pins and pwm to stop.
    """  
    def stop(self):
        logger.info("Motors stop")
        self.setPwm(self.m1Pin, self.STOP_DUTY_CYCLE)
        self.setPwm(self.m2Pin, self.STOP_DUTY_CYCLE)