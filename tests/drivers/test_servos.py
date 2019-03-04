import pigpio

from src.contest.drivers.servos import Servo

class TestServo:
    def test_pin_mode_pwm(self):
        assert Servo.PIN_MODE_PWM == pigpio.ALT5

    def test_init_with_defaults(self):
        servo = Servo()
        assert servo.pin == 12
