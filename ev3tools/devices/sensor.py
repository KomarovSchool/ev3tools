# my_ev3_package/devices/sensor.py

class RemoteUltrasonicSensor:
    def __init__(self, client, port_str):
        self._client = client
        self._port_str = port_str

    def distance(self):
        """
        Returns distance measured by the ultrasonic sensor.
        """
        return self._client.call(self._port_str, method_name='distance', args=[], kwargs={})


class RemoteGyroSensor:
    def __init__(self, client, port_str):
        self._client = client
        self._port_str = port_str

    def angle(self):
        """
        Returns gyro angle.
        """
        return self._client.call(self._port_str, method_name='angle', args=[], kwargs={})


class RemoteColorSensor:
    def __init__(self, client, port_str):
        self._client = client
        self._port_str = port_str

    def color(self):
        """
        Returns current color reading.
        """
        return self._client.call(self._port_str, method_name='color', args=[], kwargs={})
