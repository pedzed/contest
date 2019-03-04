import sys
import subprocess
from pathlib import Path

from src.contest.app import App

class Jlink:
    """Flasher for the J-Link

    Datasheet:
        https://www.segger.com/downloads/jlink/UM08001
    """
    JLINK_EXE = "JLinkExe"
    COMMAND_FILE_PATH = App.TEMP_DIR_PATH / "commandfile.jlink"
    EXPECTED_STDOUT_OK_COUNT = 2

    def __init__(self):
        self.device = "NRF52832_XXAA"
        self.offset = 0x0
        self.interface = "SWD"
        self.binaryFilePath = None
        self.speedInKiloHertz = 4000
        self.output = []

    def flash(self):
        """Flash the program by using the J-Link Commander

        Returns:
            bool -- Whether the flashing succeeded or not.
        """
        self._populateCommandFile()
        process = self._runJlinkCommander()

        return self._hasFlashSucceeded(process.stdout.readlines())

    def _populateCommandFile(self):
        commandFile = str(self.COMMAND_FILE_PATH)

        self._createCommandFileDirectoryIfMissing()

        with open(commandFile, "w+") as fileHandle:
            if str(self.binaryFilePath).endswith(".hex"):
                fileHandle.write("loadfile {}\r\n".format(self.binaryFilePath))
            else:
                if self.offset is not None:
                    fileHandle.write("loadbin {}, 0x{:X}\r\n".format(self.binaryFilePath, self.offset))
                else:
                    raise Exception("Offset required for non-hex file.")

            fileHandle.write("r\r\n") # Resets and halts the target
            fileHandle.write("go\r\n") # Starts the CPU core.
            fileHandle.write("exit\r\n")

    def _createCommandFileDirectoryIfMissing(self):
        if not self.COMMAND_FILE_PATH.parent.exists():
            self.COMMAND_FILE_PATH.parent.mkdir(parents=True)

    def _runJlinkCommander(self):
        return subprocess.Popen([
            self.JLINK_EXE,
            "-If", self.interface,
            "-Device", self.device,
            "-Speed", str(self.speedInKiloHertz),
            "-CommandFile", str(self.COMMAND_FILE_PATH),
        ], stdout=subprocess.PIPE)

    def _hasFlashSucceeded(self, outputLines):
        okCount = 0

        for line in outputLines:
            lineString = line.rstrip().decode(sys.stdout.encoding)
            self.output.append(lineString)

            if "O.K." in lineString:
                okCount += 1

        if okCount is self.EXPECTED_STDOUT_OK_COUNT:
            return True

        return False
