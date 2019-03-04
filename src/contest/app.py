import pigpio
import tempfile
from pathlib import Path

class App:
    """The central container to store one-instance objects
    """
    NAME = "ConTest"

    CONTEST_ROOT_PATH = Path(__file__).parent.parent.parent
    TEMP_DIR_PATH = Path(tempfile.gettempdir()) / NAME.lower()

    PIGPIO = pigpio
    DEVICE = PIGPIO.pi()
