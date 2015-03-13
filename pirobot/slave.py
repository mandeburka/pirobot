# coding: utf-8
import zmq

from pirobot import PORT, REQUEST_TIMEOUT, STOP
from pirobot.robot import Robot

context = zmq.Context()

socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % PORT)

poll = zmq.Poller()
poll.register(socket, zmq.POLLIN)

robot = Robot()

while True:
    socks = dict(poll.poll(REQUEST_TIMEOUT))
    if socks.get(socket) == zmq.POLLIN:
        #  Wait for next request from client
        command = socket.recv_pyobj()
        send = True
    else:
        command = {STOP}
        send = False

    print "Command: ", command

    result = robot.execute(command)

    if send:
        socket.send_pyobj(result)
