# coding: utf-8
from Queue import Empty
from multiprocessing import Process, Queue

import zmq

from pirobot.config import HOST, REQUEST_TIMEOUT, PORT, HEARTBEAT_INTERVAL
from pirobot import NOOP


class Talk(Process):
    client = None
    context = None
    poll = None

    def __init__(self):
        super(Talk, self).__init__()
        self.queue = Queue()
        self.daemon = True

    def run(self):
        self.context = zmq.Context()
        self.poll = zmq.Poller()
        self.connect()
        while True:
            try:
                request = self.queue.get(timeout=HEARTBEAT_INTERVAL)
            except Empty:
                request = {NOOP}
            self.client.send_pyobj(request)

            socks = dict(self.poll.poll(REQUEST_TIMEOUT))

            if socks.get(self.client) == zmq.POLLIN:
                reply = self.client.recv()
            else:
                print 'reconnect'
                # clear queue
                while not self.queue.empty():
                    self.queue.get()
                # Socket is confused. Close and remove it.
                self.close_connection()
                # Create new connection
                self.connect()
                continue

    def connect(self):
        self.client = self.context.socket(zmq.PAIR)
        self.client.connect("tcp://{host}:{port}".format(
            host=HOST,
            port=PORT
        ))
        self.poll.register(self.client, zmq.POLLIN)

    def close_connection(self):
        self.client.setsockopt(zmq.LINGER, 0)
        self.client.close()
        self.poll.unregister(self.client)

