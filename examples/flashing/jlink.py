from pathlib import Path

from src.contest.app import App
from src.contest.flashing.jlink import Jlink

def testFlashing():
    jlink = Jlink()
    jlink.binaryFilePath = App.CONTEST_ROOT_PATH / "tests/bins/mbed-os-example-blinky.NRF52_DK.bin"
    # jlink.binaryFilePath = App.CONTEST_ROOT_PATH / "tests/bins/mbed-os-example-blinky.NRF52_DK-2.bin"

    successfullyFlashed = jlink.flash()

    for line in jlink.output:
        print(line)

    assert successfullyFlashed
