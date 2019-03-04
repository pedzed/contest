import automationhat
import time
import json
import pytest
from pathlib import Path

from src.contest.app import App
from src.contest.drivers.servos import Servo
from src.contest.drivers.ttn_data_storage import TtnDataStorage

configFile = str(Path(__file__).parent.resolve()) + "/officehawk.config.json"
with open(configFile, "r") as f:
    App.config = json.load(f)

App.HAT = automationhat
App.ttnDataStorage = TtnDataStorage(
    appId=App.config['ttn']['app_name'],
    key=App.config['ttn']['access_key']
)

@pytest.mark.parametrize("i", range(5))
def testButton(i):
    simulateButton()
    time.sleep(1.2)

    request = App.ttnDataStorage.sendQueryRequest(App.config['ttn']['device_id'], "20s")

    event = None

    if (request.text):
        data = json.loads(request.text)
        event = data[-1]['event']
    else:
        print("[Button] request.text has no body")

    assert event == "button"
    time.sleep(3)

def simulateButton():
    servo = Servo(
        minPulseWidth=550,
        maxPulseWidth=2230,
    )

    untriggerAngle = 90
    triggerAngle = 15

    servo.setAngle(untriggerAngle)
    time.sleep(2)

    servo.setAngle(triggerAngle)
    time.sleep(.3)

    servo.setAngle(untriggerAngle)

@pytest.mark.parametrize("i", range(3))
def testAccelerometer(i):
    simulateAccelerometer()
    time.sleep(1.2)

    request = App.ttnDataStorage.sendQueryRequest(App.config['ttn']['device_id'], "20s")

    event = None

    if (request.text):
        data = json.loads(request.text)
        event = data[-1]['event']
    else:
        print("[Accelerometer] request.text has no body")

    assert event == "activity"
    time.sleep(3)

def simulateAccelerometer():
    App.HAT.output.one.on()
    time.sleep(2)

    App.HAT.output.one.off()
