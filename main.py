#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

from threading import Thread
import sys
import time
import random

run = True

class CircleDriveBase(DriveBase):

    def __init__(self, left_motor, right_motor, wheel_diameter, axle_track):
        super().__init__(left_motor, right_motor, wheel_diameter, axle_track)

    def circle(self, segment_len, num_segments=36):
        assert num_segments <= 360
        for i in range(num_segments):
            if run:
                self.straight(segment_len)
                self.turn(360/num_segments)


def sound(ev3):
    per_freq_duration = 0.1
    while run:
        freq_range = range(random.randint(0,200), random.randint(200, 1000))
        for i in freq_range:
            ev3.speaker.beep(frequency=i, duration=per_freq_duration)
        for i in reversed(freq_range):
            ev3.speaker.beep(frequency=i, duration=per_freq_duration)


def display(ev3):
    while run:
        for _ in range(random.randint(2, 10)):
            xpos = random.randint(0, 150)
            ypos = random.randint(0, 200)
            rad = random.randint(10, 100)
            ev3.screen.draw_circle(xpos, ypos, rad)
            time.sleep(0.5)
        ev3.screen.clear()


def drive(ev3):
    robot = CircleDriveBase(
        Motor(Port.B), Motor(Port.C), 55.5, 104
    )
    robot.settings(1000, 1000, 1000, 1000)
    while run:
        robot.circle(random.randint(0, 300))


def main():
    ev3 = EV3Brick()
    for thread in [
        # Thread(target=sound, args=(ev3,)),
        Thread(target=display, args=(ev3,)),
        Thread(target=drive, args=(ev3,)),
    ]:
        thread.start()
    while True:
        if any(EV3Brick.buttons.pressed()):
            run = False
            print("Killed by a button")
            sys.exit()


if __name__ == "__main__":
    main()
