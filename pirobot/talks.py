# coding: utf-8
from multiprocessing import Process, Queue
import zmq
from pirobot import REQUEST_TIMEOUT, PORT


class Talks(Process):
    client = None
    context = None
    poll = None

    def __init__(self):
        super(Talks, self).__init__()
        self.queue = Queue()
        self.daemon = True

    def run(self):
        self.context = zmq.Context()
        self.poll = zmq.Poller()
        self.connect()

        while True:
            request = self.queue.get()
            self.client.send_pyobj(request)

            socks = dict(self.poll.poll(REQUEST_TIMEOUT))

            if socks.get(self.client) == zmq.POLLIN:
                reply = self.client.recv()
            else:
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
        self.client.connect("tcp://localhost:%s" % PORT)
        self.poll.register(self.client, zmq.POLLIN)

    def close_connection(self):
        self.client.setsockopt(zmq.LINGER, 0)
        self.client.close()
        self.poll.unregister(self.client)
