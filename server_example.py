#!/usr/bin/env pybricks-micropython
from ev3tools.server import EV3RPCServer


def main():
    server = EV3RPCServer()
    server.start()


if __name__ == '__main__':
    main()
