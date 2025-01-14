# my_ev3_package/server.py

import usocket as socket  # or just 'import socket' depending on environment
import ujson as json      # or 'import json'
import _thread            # or 'import threading' if available
from pybricks.parameters import Port
from pybricks.ev3devices import (Motor, UltrasonicSensor, GyroSensor, ColorSensor)
# etc., import any other Pybricks classes you need

from .common import str2port, str2class



class EV3RPCServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self._host = host
        self._port = port
        self._devices = {}  # { 'A': Motor instance, 'S1': UltrasonicSensor instance, ... }

    def start(self):
        """
        Start the server, accept connections, handle requests (blocking).
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = socket.getaddrinfo(self._host, self._port)[0][-1]
        s.bind(addr)
        s.listen(1)
        print("Listening on {}:{}...".format(self._host, self._port))
        while True:
            client_socket, addr = s.accept()
            print("Client connected from {}".format(addr))
            # If you want to handle multiple clients, spawn a thread
            # For now, we will just handle one client at a time
            self.handle_client(client_socket)
            client_socket.close()
            print("Client disconnected.")

    def handle_client(self, client_socket):
        """
        Reads lines from the client until it disconnects.
        """
        while True:
            try:
                line = self._recv_line(client_socket)
                if not line:
                    break
                print(line)
                request = json.loads(line)
                response = self._handle_request(request)
                # Send response back
                client_socket.write(json.dumps(response).encode('utf-8') + b"\n")
            except OSError:
                break
            except Exception as e:
                # If something else fails, send an error response
                err_msg = {"error": str(e)}
                client_socket.write(json.dumps(err_msg).encode('utf-8') + b"\n")

    def _handle_request(self, request):
        """
        Dispatch the request based on 'type' (init/call).
        """
        req_type = request.get("type")
        if req_type == "init":
            return self._handle_init(request)
        elif req_type == "call":
            return self._handle_call(request)
        else:
            return {"error": "Unknown request type {}".format(req_type)}

    def _handle_init(self, request):
        port_str = request["port"]
        device_str = request["device"]
        # Convert the port string to an actual Port enum
        port = str2port(port_str)
        # Convert device string to class name
        class_name = str2class(device_str)

        # Dynamically construct device instance
        if class_name == "Motor":
            self._devices[port_str] = Motor(port)
        elif class_name == "UltrasonicSensor":
            self._devices[port_str] = UltrasonicSensor(port)
        elif class_name == "GyroSensor":
            self._devices[port_str] = GyroSensor(port)
        elif class_name == "ColorSensor":
            self._devices[port_str] = ColorSensor(port)
        else:
            return {"error": "Unknown device {}".format(device_str)}

        return {"result": None}

    def _handle_call(self, request):
        port_str = request["port"]
        method_name = request["method"]
        args = request.get("args", [])
        kwargs = request.get("kwargs", {})

        # Fetch device
        device = self._devices.get(port_str)
        if not device:
            return {"error": "No device initialized on port {}".format(port_str)}

        # Call method
        if not hasattr(device, method_name):
            return {"error": "Device on port {} has no method {}".format(port_str, method_name)}

        method = getattr(device, method_name)
        result = method(*args, **kwargs)
        # If method returned something, we include it in response
        return {"result": result}

    def _recv_line(self, client_socket):
        """
        Read until newline (simple approach).
        """
        buf = b""
        while True:
            chunk = client_socket.recv(1)
            if not chunk:
                return None
            buf += chunk
            if b"\n" in buf:
                break
        return buf.strip().decode('utf-8')

