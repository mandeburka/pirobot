# coding: utf-8
from pirobot import STOP, MOVE_LEFT, MOVE_RIGHT, MOVE_BACKWARD, MOVE_FORWARD
from pirobot.communication.listen import Listen
import rrb2


class Robot(object):
    speed = 1

    def __init__(self):
        self.rrb2 = rrb2.RRB2()

    def execute(self, commands):
        if STOP in commands:
            self.rrb2.stop()
        elif MOVE_RIGHT in commands:
            self.rrb2.right(speed=self.speed)
        elif MOVE_LEFT in commands:
            self.rrb2.left(speed=self.speed)
        elif MOVE_FORWARD in commands:
            self.rrb2.forward(speed=self.speed)
        elif MOVE_BACKWARD in commands:
            self.rrb2.reverse(speed=self.speed)

if __name__ == '__main__':
    robot = Robot()
    listen = Listen(callback=robot.execute)
    listen.run()
