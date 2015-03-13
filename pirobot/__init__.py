# coding: utf-8
PORT = "5556"

REQUEST_TIMEOUT = 1000
HEARTBEAT_INTERVAL = REQUEST_TIMEOUT / 2000.0

MOVE_FORWARD = 'FORWARD'
MOVE_BACKWARD = 'BACKWARD'
MOVE_RIGHT = 'RIGHT'
MOVE_LEFT = 'LEFT'
STOP = 'STOP'
NOOP = 'NOOP'

MOVEMENTS = (MOVE_FORWARD, MOVE_BACKWARD, MOVE_RIGHT, MOVE_LEFT)
