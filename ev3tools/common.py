# my_ev3_package/common.py

from pybricks.parameters import Port

# Mapping from Pybricks Ports to strings
def port2str(port: Port) -> str:
    """
    Convert a Pybricks Port enum to a string like "A" or "S1".
    """
    # This is a naive example; adapt logic if necessary
    if port in [Port.A, Port.B, Port.C, Port.D]:
        return port.name  # e.g. Port.A -> "A"
    elif port in [Port.S1, Port.S2, Port.S3, Port.S4]:
        return port.name  # e.g. Port.S1 -> "S1"
    else:
        raise ValueError("Unsupported port: {}".format(port))

def str2port(port_str: str) -> Port:
    """
    Convert "A", "B", "C", "D", "S1", "S2", etc. back to Pybricks Port enums.
    """
    # This is a naive example; adapt logic if necessary
    return getattr(Port, port_str)  # e.g. "A" -> Port.A, "S1" -> Port.S1

# Example device class name mapping
DEVICE_CLASS_MAP = {
    'motor': 'Motor',
    'ultrasonic': 'UltrasonicSensor',
    'gyro': 'GyroSensor',
    'color': 'ColorSensor',
}

def class2str(device_class_name: str) -> str:
    """
    Convert a device class (e.g. "Motor") into a device string (e.g. "motor").
    """
    for key, val in DEVICE_CLASS_MAP.items():
        if val == device_class_name:
            return key
    raise ValueError("No known device string for class {}".format(device_class_name))

def str2class(device_str: str) -> str:
    """
    Convert a device string (e.g. "motor") into a device class name (e.g. "Motor").
    """
    if device_str in DEVICE_CLASS_MAP:
        return DEVICE_CLASS_MAP[device_str]
    else:
        raise ValueError("No known device class for string {}".format(device_str))
