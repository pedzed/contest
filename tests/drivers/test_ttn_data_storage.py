import pytest
import requests

from src.contest.drivers.ttn_data_storage import TtnDataStorage

class TestTtnDataStorage:
    APP_ID = "contest-unittest"
    KEY = "ttn-account-v2.QZbD00AVneqfidn3bS7k37xC77p4BDS2xVzifpQYdcs"

    def test_init_empty_arguments(self):
        with pytest.raises(TypeError):
            TtnDataStorage()

    def test_init_correct_arguments(self):
        dataStorage = TtnDataStorage("app_id_123", "access_key_123")

        assert dataStorage.appId == "app_id_123"
        assert dataStorage.accessKey == "access_key_123"

    def test_request_with_invalid_app_id(self):
        dataStorage = TtnDataStorage("app_id_123", "access_key_123")
        request = dataStorage.sendDevicesRequest()
        assert request.status_code == 404

    def test_request_with_invalid_access_key(self):
        dataStorage = TtnDataStorage("office-hawk", "access_key_123")
        request = dataStorage.sendDevicesRequest()
        assert request.status_code == 401

    def test_valid_send_devices_request(self):
        dataStorage = TtnDataStorage(self.APP_ID, self.KEY)
        request = dataStorage.sendDevicesRequest()
        assert request.status_code in [200, 204]

    def test_invalid_send_query_request(self):
        dataStorage = TtnDataStorage(self.APP_ID, self.KEY)
        request = dataStorage.sendQueryRequest(deviceId="***NON-EXISTENT***")
        assert request.status_code == 400

    def test_send_query_request_without_specified_device_and_without_registered_devices(self):
        """NOTE: It is assumed that the registered TTN app has no registered devices!
        """
        dataStorage = TtnDataStorage(self.APP_ID, self.KEY)
        request = dataStorage.sendQueryRequest()
        assert request.status_code == 204

    def test_send_query_all_request_without_registered_devices(self):
        dataStorage = TtnDataStorage(self.APP_ID, self.KEY)
        request = dataStorage.sendQueryAllRequest()
        assert request.status_code == 204
