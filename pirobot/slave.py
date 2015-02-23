# coding: utf-8
import zmq

from pirobot import PORT

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % PORT)

while True:
     #  Wait for next request from client
    message = socket.recv_pyobj()
    print "Received request: ", message
    socket.send("World from %s" % PORT)
