# my_ev3_package/devices/motor.py

class RemoteMotor:
    def __init__(self, client, port_str):
        """
        Client is an instance of the TCP client that knows how to send JSON messages.
        port_str is something like 'A'.
        """
        self._client = client
        self._port_str = port_str

    def run(self, speed):
        """
        Runs the motor at the specified speed (degrees/s).
        Example usage: motor.run(100)
        """
        return self._client.call(self._port_str, method_name='run', args=[speed], kwargs={})

    def angle(self):
        """
        Returns the current measured angle of the motor's rotation.
        """
        return self._client.call(self._port_str, method_name='angle', args=[], kwargs={})

    def stop(self):
        """
        Stop the motor
        """
        return self._client.call(self._port_str, method_name='stop', args=[], kwargs={})
