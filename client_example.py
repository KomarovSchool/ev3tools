

from ev3tools.client import RemoteHub


hub = RemoteHub("10.42.0.30")

motor = hub.motor("A")
motor.dc(100)
