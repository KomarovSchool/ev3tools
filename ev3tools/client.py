# my_ev3_package/client.py

import socket
import json
from my_ev3_package.common import port2str, class2str, str2port
from my_ev3_package.devices.motor import RemoteMotor
from my_ev3_package.devices.sensor import (
    RemoteUltrasonicSensor,
    RemoteGyroSensor,
    RemoteColorSensor,
)

class RemoteHub:
    """
    Represents a remote EV3 hub we can control over TCP.
    """
    def __init__(self, ip, port=12345):
        self.ip = ip
        self.port = port
        # We can open/close connection per call or keep it open
        # For simplicity, let’s keep it open once connected
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self.ip, self.port))

    def motor(self, pybricks_port):
        """
        Initialize a remote motor on a port (Port.A, Port.B, etc.).
        This sends an 'init' command to the server.
        """
        port_str = port2str(pybricks_port)
        device_str = class2str("Motor")
        self._init_device(port_str, device_str)
        return RemoteMotor(self, port_str)

    def ultrasonic(self, pybricks_port):
        port_str = port2str(pybricks_port)
        device_str = class2str("UltrasonicSensor")
        self._init_device(port_str, device_str)
        return RemoteUltrasonicSensor(self, port_str)

    def gyro(self, pybricks_port):
        port_str = port2str(pybricks_port)
        device_str = class2str("GyroSensor")
        self._init_device(port_str, device_str)
        return RemoteGyroSensor(self, port_str)

    def color(self, pybricks_port):
        port_str = port2str(pybricks_port)
        device_str = class2str("ColorSensor")
        self._init_device(port_str, device_str)
        return RemoteColorSensor(self, port_str)

    def _init_device(self, port_str, device_str):
        """
        Sends an 'init' command to the server so it can create
        the actual Pybricks object for the device.
        """
        request = {
            "type": "init",
            "port": port_str,
            "device": device_str
        }
        self._send_and_receive(request)

    def call(self, port_str, method_name, args, kwargs):
        """
        Sends a 'call' command to the server.
        """
        request = {
            "type": "call",
            "port": port_str,
            "method": method_name,
            "args": args,
            "kwargs": kwargs
        }
        response = self._send_and_receive(request)
        return response.get("result", None)

    def _send_and_receive(self, request_dict):
        """
        Send the request as JSON and wait for the JSON response.
        """
        data = json.dumps(request_dict).encode('utf-8')
        # You might want a length-prefix or something more robust in real code
        self._sock.sendall(data + b"\n")  # Send a newline as delimiter
        # Now receive response
        response_data = self._recv_line()
        return json.loads(response_data)

    def _recv_line(self):
        """
        Very basic loop to read until newline.
        """
        buffer = b""
        while True:
            chunk = self._sock.recv(1)
            if not chunk:
                raise ConnectionError("Disconnected")
            buffer += chunk
            if b"\n" in buffer:
                break
        return buffer.strip().decode('utf-8')

    def close(self):
        """
        Close the TCP socket.
        """
        self._sock.close()
