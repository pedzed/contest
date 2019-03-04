import pigpio

from src.contest.app import App

class TestApp:
    def test_app_name(self):
        assert App.NAME == "ConTest"

    def test_temp_dir_path(self):
        tempDir = str(App.TEMP_DIR_PATH)
        assert tempDir == "/tmp/contest"

    def test_device(self):
        assert type(App.DEVICE) is type(pigpio.pi())
