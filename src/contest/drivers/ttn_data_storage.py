import requests

class TtnDataStorage:
    def __init__(self, appId, key):
        """
        Arguments:
            appId {str} -- The TTN app_id
            key {str} -- The TTN application access key
        """
        self.apiBaseUri = "https://" + appId + ".data.thethingsnetwork.org/api/v2"
        self.appId = appId
        self.accessKey = key

    def sendDevicesRequest(self):
        """The list of devices for which data has been stored

        Returns:
            Response -- The HTTP response
        """
        return requests.get(
            url=self._constructEndpoint("/devices"),
            headers={
                "Authorization": "key " + self.accessKey
            }
        )

    def _constructEndpoint(self, uri):
        """Get the full endpoint URL based on the given URI

        Arguments:
            uri {str} -- The URI to the endpoint

        Returns:
            str -- The endpoint URI
        """
        return self.apiBaseUri + uri

    def sendQueryRequest(self, deviceId=None, timeLimit="30s"):
        """Query the data for all devices or a specific device

        Keyword Arguments:
            timeLimit {str} -- Limit data to X ago (default: {"30s"})

        Returns:
            Response -- The HTTP response
        """
        if (deviceId is None):
            return self.sendQueryAllRequest(timeLimit)

        return requests.get(
            url=self._constructEndpoint("/query/" + deviceId),
            headers={
                "Authorization": "key " + self.accessKey
            },
            params={
                "last": timeLimit,
            },
        )

    def sendQueryAllRequest(self, timeLimit="30s"):
        """Query the data for all devices

        Keyword Arguments:
            timeLimit {str} -- Limit data to X ago (default: {"30s"})

        Returns:
            Response -- The HTTP response
        """
        return requests.get(
            url=self._constructEndpoint("/query"),
            headers={
                "Authorization": "key " + self.accessKey
            },
            params={
                "last": timeLimit,
            },
        )
