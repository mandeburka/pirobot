# coding: utf-8
import zmq

from pirobot import STOP
from pirobot.config import PORT, REQUEST_TIMEOUT


class Listen(object):
    def __init__(self, callback):
        self.callback = callback
        self.context = zmq.Context()

        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind("tcp://*:%s" % PORT)

        self.poll = zmq.Poller()
        self.poll.register(self.socket, zmq.POLLIN)

    def run(self):
        while True:
            socks = dict(self.poll.poll(REQUEST_TIMEOUT))
            if socks.get(self.socket) == zmq.POLLIN:
                #  Wait for next request from client
                command = self.socket.recv_pyobj()
                send = True
            else:
                command = {STOP}
                send = False

            print "Command: ", command

            result = self.callback(command)

            if send:
                self.socket.send_pyobj(result)
