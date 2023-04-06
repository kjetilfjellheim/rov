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
    STOP_DUTY_CYCLE = 0
    HIGH = 1
    LOW = 0

    """
    Class variables
    """
    pwm1Pin = None    #Pwm pin for motor 1
    m1Pin = None      #Motor pin for motor 1
    m2Pin = None      #Motor pin for motor 2
    pwm2Pin = None    #Pwm pin for motor 2
    
    def __init__(self, pwm1Pin, m1Pin, m2Pin, pwm2Pin):
        logger.info("Starting initalizing LM298")
        self.pwm1Pin = pwm1Pin
        self.m1Pin = m1Pin
        self.m2Pin = m2Pin
        self.pwm2Pin = pwm2Pin
        self.stop()
        logger.info("Finished initalizing LM298")

    def setForward(self, mPin):
        mPin.write(self.HIGH)
        if mPin == self.m1Pin:
            logger.info("Motor 1 written value HIGH")
        elif mPin == self.m2Pin:
            logger.info("Motor 2 written value HIGH")

    def setReverse(self, mPin):
        mPin.write(self.LOW)
        if mPin == self.m1Pin:
            logger.info("Motor 1 written value LOW")
        elif mPin == self.m2Pin:
            logger.info("Motor 2 written value LOW")        

    """
    Setting pwm value on motor. The value is a fraction between 0-1.
    """        
    def setPwm(self, pwm, value):
        writeVal = value / 100.0
        pwm.write(writeVal)
        if pwm == self.pwm1Pin:
            logger.info("PWM motor 1 written value {0} dutycycle set {1}".format(writeVal, value))
        elif pwm == self.pwm2Pin:
            logger.info("PWM motor 2 written value {0} dutycycle set {1}".format(writeVal, value))               

    """
    Rotate in place by setting one motor forward and he other back at the same speed.
    """  
    def rotateInPlace(self, speed, direction):
        if self.DIRECTION_LEFT == direction:
            self.setReverse(self.m1Pin)
            self.setForward(self.m2Pin)
        else:
            self.setForward(self.m1Pin)
            self.setReverse(self.m2Pin)        
        logger.info("Motors rotate in place")
        self.setPwm(self.pwm1Pin, 50 + (speed / 2))
        self.setPwm(self.pwm2Pin, 50 + (speed / 2))

    """
    Turn by setting left and right motors at different speed.
    """  
    def turnDifferential(self, speedLeft, speedRight, direction):
        logger.info("Motors turn differential")
        if self.DIRECTION_FORWARD == direction:
            self.setForward(self.m1Pin)
            self.setForward(self.m2Pin)
        else:
            self.setReverse(self.m1Pin)
            self.setReverse(self.m2Pin)
        self.setPwm(self.pwm1Pin, 50 + (speedLeft / 2))
        self.setPwm(self.pwm2Pin, 50 + (speedRight / 2))

    """
    Move forward or back
    """  
    def forward(self, speed, direction):
        logger.info("Motors forward/reverse")
        if self.DIRECTION_FORWARD == direction:
            self.setForward(self.m1Pin)
            self.setForward(self.m2Pin)
        else:
            self.setReverse(self.m1Pin)
            self.setReverse(self.m2Pin)
        self.setPwm(self.pwm1Pin, 50 + (speed / 2))
        self.setPwm(self.pwm2Pin, 50 + (speed / 2))
    
    """
    Stop both motors by disbaling enable pins and pwm to stop.
    """  
    def stop(self):
        logger.info("Motors stop")
        self.setReverse(self.m1Pin)
        self.setReverse(self.m2Pin)        
        self.setPwm(self.pwm1Pin, self.STOP_DUTY_CYCLE)
        self.setPwm(self.pwm2Pin, self.STOP_DUTY_CYCLE)