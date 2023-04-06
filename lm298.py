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
    DIRECTION_LEFT = -1
    DIRECTION_RIGHT = 1
    DIRECTION_FORWARD = 1
    DIRECTION_BACK = -1
    STOP_DUTY_CYCLE = 50
    NEGATE = -1
    ON = 1
    OFF = 0

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
        self.e1Pin.write(self.ON)
        self.e2Pin.write(self.ON)
        logger.info("Enabled motors LM298")

    def disableMotors(self):
        self.e1Pin.write(self.OFF)
        self.e2Pin.write(self.OFF)
        logger.info("Disabled motors LM298")
        
    def setPwm(self, pwm, dutyCycle):
        pwm.write(dutyCycle / 100)
        if pwm == self.m1Pin:
            logger.info("PWM motor 1 dutycycle set {0}".format(dutyCycle))
        else:
            logger.info("PWM motor 2 dutycycle set {0}".format(dutyCycle))

    def rotateInPlace(self, speed, direction):
        self.enableMotors()
        self.setPwm(self.m1Pin, 100 - (50 + (speed * direction / 2)))
        self.setPwm(self.m2Pin, 100 - (50 + (speed * direction / 2)))

    def turnDifferential(self, speedLeft, speedRight, direction):
        logger.info("Motors turn differential")
        self.enableMotors()
        self.setPwm(self.m1Pin, 100 - (50 + (speedLeft * direction / 2)))
        self.setPwm(self.m2Pin, 100 - (50 - (speedRight * direction / 2)))

    def forward(self, speed, direction):
        logger.info("Motors forward/reverse")
        self.enableMotors()
        self.setPwm(self.m1Pin, 100 - (50 + (speed * direction / 2)))
        self.setPwm(self.m2Pin, 100 - (50 - (speed * direction / 2)))

    def stop(self):
        logger.info("Motors stop")
        self.disableMotors()
        self.setPwm(self.m1Pin, self.STOP_DUTY_CYCLE)
        self.setPwm(self.m2Pin, self.STOP_DUTY_CYCLE)