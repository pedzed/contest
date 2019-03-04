import time
from src.contest.app import App

class Servo:
    PIN_MODE_PWM = App.PIGPIO.ALT5

    def __init__(self,
        pin=12,
        minPulseWidth=500,
        maxPulseWidth=2500,
        minAngle=0,
        maxAngle=180
    ):
        self.pin = pin
        self.minPulseWidth = minPulseWidth
        self.maxPulseWidth = maxPulseWidth
        self.minAngle = minAngle
        self.maxAngle = maxAngle

        App.DEVICE.set_mode(self.pin, self.PIN_MODE_PWM)

    def setPulseWidth(self, value):
        """Control the servo mechanically based on the given pulse width.

        Arguments:
            value {int} -- The pulse width

        Raises:
            Exception -- Out of range
        """
        if value < self.minPulseWidth or value > self.maxPulseWidth:
            raise Exception("Pulse width ({}) must be between {} and {}.".format(
                value,
                self.minPulseWidth,
                self.maxPulseWidth
            ))

        App.DEVICE.set_servo_pulsewidth(self.pin, value)

    def getPulseWidth(self):
        """
        Returns:
            int -- The pulse width
        """
        return App.DEVICE.get_servo_pulsewidth(self.pin)

    def setAngle(self, value):
        """Map the requested angle to its related pulse width and rotate the servo.

        Arguments:
            value {int} -- The angle

        Raises:
            Exception -- Out of range
        """
        if value < self.minAngle or value > self.maxAngle:
            raise Exception("Angle ({}) must be between {} and {}.".format(
                value,
                self.minAngle,
                self.maxAngle
            ))

        pulseWidth = self._mapMinMaxFromTo(
            value,
            (self.minAngle, self.maxAngle),
            (self.minPulseWidth, self.maxPulseWidth)
        )
        self.setPulseWidth(pulseWidth)

    def getAngle(self):
        """
        Returns:
            int -- The angle
        """
        pulseWidth = self._mapMinMaxFromTo(
            self.getPulseWidth(),
            (self.minPulseWidth, self.maxPulseWidth),
            (self.minAngle, self.maxAngle)
        )
        return pulseWidth

    def _mapMinMaxFromTo(self, value, fromMinMax, toMinMax):
        """Map a value from a given min/max to another min/max.

        E.g. map 0-360 degrees to 0-100%

        Read more:
            https://www.arduino.cc/reference/en/language/functions/math/map/

        Arguments:
            value {float} -- The number to modify
            fromMinMax {tuple} -- The 'from' min and max values
            toMinMax {tuple} -- The 'to' min and max values

        Returns:
            float -- The modified value
        """
        (fromMin, fromMax) = fromMinMax
        (toMin, toMax) = toMinMax

        return (value - fromMin) * (toMax - toMin) / (fromMax - fromMin) + toMin
