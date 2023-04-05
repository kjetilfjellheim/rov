import logging
import pyfirmata

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
    PWM_FREQUENCY = 1000
    DIRECTION_LEFT = 1
    DIRECTION_RIGHT = -1
    DIRECTION_FORWARD = 1
    DIRECTION_BACK = -1
    STOP_DUTY_CYCLE = 50
    NEGATE = -1

    """
    Class variables
    """
    e1Pin = None
    m1Pin = None
    e2Pin = None
    m2Pin = None

    def __init__(self, e1Pin, m1Pin, m2Pin, e2Pin):
        logger.info("Starting initalizing LM298")
        self.e1Pin = e1Pin
        self.m1Pin = m1Pin
        self.m2Pin = m2Pin
        self.e2Pin = e2Pin
        self.stop()
        logger.info("Finished initalizing LM298")

    def enableMotors(self):
        self.e1Pin.write(1)
        self.e2Pin.write(1)
        logger.info("Enabled motors LM298")

    def disableMotors(self):
        self.e1Pin.write(0)
        self.e2Pin.write(0)
        logger.info("Disabled motors LM298")
        
    def setPwm(self, pwm, dutyCycle):
        pwm.write(dutyCycle / 100)
        if pwm == self.m1Pin:
            logger.info("PWM motor 1 dutycycle set {0}".format(dutyCycle))
        else:
            logger.info("PWM motor 2 dutycycle set {0}".format(dutyCycle))

    def rotateInPlace(self, speed, direction):
        self.enableMotors()
        self.setPwm(self.m1Pin, speed * direction)
        self.setPwm(self.m2Pin, speed * direction)

    def turnDifferential(self, speedLeft, speedRight):
        logger.info("Motors turn differential")
        self.enableMotors()
        self.setPwm(self.m1Pin, speedLeft)
        self.setPwm(self.m2Pin, speedRight * self.NEGATE)

    def forward(self, speed, direction):
        logger.info("Motors forward/reverse")
        self.enableMotors()
        self.setPwm(self.m1Pin, speed * direction)
        self.setPwm(self.m2Pin, speed * self.NEGATE * direction)

    def stop(self):
        logger.info("Motors stop")
        self.disableMotors()
        self.setPwm(self.m1Pin, self.STOP_DUTY_CYCLE)
        self.setPwm(self.m2Pin, self.STOP_DUTY_CYCLE)