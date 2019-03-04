from pathlib import Path

from src.contest.flashing.jlink import Jlink

class TestJlink:
    def test_default_jlink_exe_path(self):
        assert Jlink.JLINK_EXE == "JLinkExe"

    def test_default_device(self):
        jlink = Jlink()
        assert jlink.device == "NRF52832_XXAA"

    def test_default_offset(self):
        jlink = Jlink()
        assert jlink.offset == 0x0

    def test_default_interface(self):
        jlink = Jlink()
        assert jlink.interface == "SWD"

    def test_default_binary_file_path(self):
        jlink = Jlink()
        assert jlink.binaryFilePath is None

    def test_default_speed(self):
        jlink = Jlink()
        assert jlink.speedInKiloHertz == 4000

    def test_flashing_with_no_jlink_powered(self):
        outputFile = str(Path(__file__).parent.resolve()) + "/output_jlink_not_powered.txt"

        with open(outputFile, "rb") as file:
            outputLines = file.readlines()

        jlink = Jlink()
        assert jlink._hasFlashSucceeded(outputLines) is False

    def test_flashing_with_no_connected_or_unpowered_dut(self):
        outputFile = str(Path(__file__).parent.resolve()) + "/output_jlink_not_connected_or_unpowered_dut.txt"

        with open(outputFile, "rb") as file:
            outputLines = file.readlines()

        jlink = Jlink()
        assert jlink._hasFlashSucceeded(outputLines) is False

    def test_flashing_with_already_flashing_binary(self):
        outputFile = str(Path(__file__).parent.resolve()) + "/output_binary_already_flashed.txt"

        with open(outputFile, "rb") as file:
            outputLines = file.readlines()

        jlink = Jlink()
        assert jlink._hasFlashSucceeded(outputLines) is True

    def test_flashing_with_already_flashing_binary(self):
        outputFile = str(Path(__file__).parent.resolve()) + "/output_binary_successfully_flashed.txt"

        with open(outputFile, "rb") as file:
            outputLines = file.readlines()

        jlink = Jlink()
        assert jlink._hasFlashSucceeded(outputLines) is True

    def test_command_file_population(self):
        jlink = Jlink()

        rootDir = Path(__file__).parent.parent
        jlink.binaryFilePath = rootDir / "bins/BLE_Beacon.hex"
        jlink._populateCommandFile()

        expected = [
            "loadfile {}\n".format(str(jlink.binaryFilePath)),
            "r\n",
            "go\n",
            "exit\n",
        ]

        with open(str(jlink.COMMAND_FILE_PATH), "r") as file:
            actual = file.readlines()

        assert actual == expected
