import logging
import RPi.GPIO as gpio

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

    PWM_FREQUENCY = 1000

    DIRECTION_LEFT = 1
    DIRECTION_RIGHT = -1

    DIRECTION_FORWARD = 1
    DIRECTION_BACK = -1

    STOP_DUTY_CYCLE = 50

    NEGATE = -1

    e1Pin = None
    m1Pin = None
    pwm1 = None
    e2Pin = None
    m2Pin = None
    pwm2 = None

    def __init__(self, e1Pin, m1Pin, m2Pin, e2Pin):
        logger.info("Starting initalizing LM298")
        self.e1Pin = e1Pin
        self.m1Pin = m1Pin
        self.m2Pin = m2Pin
        self.e2Pin = e2Pin
        self.pwm1 = gpio.PWM(m1Pin, self.PWM_FREQUENCY)
        self.pwm2 = gpio.PWM(m2Pin, self.PWM_FREQUENCY)
        self.stop()
        logger.info("Finished initalizing LM298")

    def enableMotors(self):
        gpio.output(self.e1Pin, gpio.HIGH)
        gpio.output(self.e2Pin, gpio.HIGH)
        logger.info("Enabled motors LM298")

    def disableMotors(self):
        gpio.output(self.e1Pin, gpio.LOW)
        gpio.output(self.e2Pin, gpio.LOW)
        logger.info("Disabled motors LM298")
        
    def setPwm(self, pwm, dutyCycle):
        pwm.ChangeDutyCycle(dutyCycle)
        if pwm == self.pwm1:
            logger.info("PWM motor 1 dutycycle set {}", dutyCycle)
        else:
            logger.info("PWM motor 2 dutycycle set {}", dutyCycle)

    def rotateInPlace(self, speed, direction):
        self.enableMotors()
        self.setPwm(self.pwm1, speed)
        self.setPwm(self.pwm2, speed)

    def turnDifferential(self, speedLeft, speedRight):
        logger.info("Motors turn differential")
        self.enableMotors()
        self.setPwm(self.pwm1, speedLeft)
        self.setPwm(self.pwm2, speedRight)

    def forward(self, speed, direction):
        logger.info("Motors forward/reverse")
        self.enableMotors()
        self.setPwm(self.pwm1, speed)
        self.setPwm(self.pwm2, speed)

    def stop(self):
        logger.info("Motors stop")
        self.disableMotors()
        self.setPwm(self.pwm1, self.STOP_DUTY_CYCLE)
        self.setPwm(self.pwm2, self.STOP_DUTY_CYCLE)