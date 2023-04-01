from machine import Pin, PWM

"""
Constants
"""
LOGGER = "lm298"

"""
Class definitions
"""
class MotorControl:

    DIRECTION_LEFT = 1
    DIRECTION_RIGHT = -1

    DIRECTION_FORWARD = 1
    DIRECTION_BACK = -1

    NEGATE = -1

    MAX_DUTY_CYCLE: int = 65535
    STOP_DUTY_CYCLE: int = 32768
    SPEED_CYCLE: int = int(STOP_DUTY_CYCLE / 100)

    e1Pin: Pin
    m1Pin: Pin
    pwm1: PWM
    e2Pin: Pin
    m2Pin: Pin
    pwm2: PWM

    def __init__(self, e1Pin, m1Pin, e2Pin, m2Pin):
        self.e1Pin = e1Pin
        self.m1Pin = m1Pin
        self.e2Pin = e2Pin
        self.m2Pin = m2Pin
        self.pwm1 = PWM(m1Pin)
        self.pwm2 = PWM(m2Pin)

    def enableMotors(self):
        self.e2Pin.value(True)
        self.e1Pin.value(True)

    def disableMotors(self):
        self.e2Pin.value(False)
        self.e1Pin.value(False)
        
    def setPwm(self, pwm, dutyCycle):
        pwm.duty_u16(dutyCycle)

    def rotateInPlace(self, speed, direction):
        self.enableMotors()
        self.setPwm(self.pwm1, int(self.STOP_DUTY_CYCLE + (direction * speed * self.SPEED_CYCLE)))
        self.setPwm(self.pwm2, int(self.STOP_DUTY_CYCLE + (direction * speed * self.SPEED_CYCLE)))

    def turnDifferential(self, speedLeft, speedRight):
        self.enableMotors()
        self.setPwm(self.pwm1, int(self.STOP_DUTY_CYCLE + (self.DIRECTION_RIGHT * speedLeft * self.SPEED_CYCLE)))
        self.setPwm(self.pwm2, int(self.STOP_DUTY_CYCLE + (self.DIRECTION_LEFT * speedRight * self.SPEED_CYCLE)))

    def forward(self, speed, direction):
        self.enableMotors()
        self.setPwm(self.pwm1, int(self.STOP_DUTY_CYCLE + (direction * speed * self.SPEED_CYCLE * self.NEGATE)))
        self.setPwm(self.pwm2, int(self.STOP_DUTY_CYCLE + (direction * speed * self.SPEED_CYCLE)))

    def stop(self):
        self.disableMotors()
        self.setPwm(self.pwm1, self.STOP_DUTY_CYCLE)
        self.setPwm(self.pwm2, self.STOP_DUTY_CYCLE)