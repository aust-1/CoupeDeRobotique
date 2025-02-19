from controllers import RollingBasisDummy, RollingBasis
from pydualsense import *
from enum import Enum
import time
from loggerplusplus import Logger, log
import os

from config_loader import CONFIG


class ControlMode(Enum):
    Manual = 0
    Auto = 1


class Client:
    def __init__(
        self,
        deadzone=5,
    ):
        self.websocket = None
        self.controller = None
        self.rolling_basis = None

        self.deadzone = deadzone

        # Auto control
        self.throttle = 0
        self.steering = 0

        self.run = True
        self.logger = Logger(
            identifier="Main",
        )
        print("Init done")

    def start(self):
        self.controller = pydualsense()
        self.controller.init()
        while self.controller.states is None:
            print(".", end="")
            time.sleep(0.1)
        self.controller.light.setPlayerID(PlayerID.PLAYER_3)

        self.controller.light.setColorI(255, 0, 0)

        self.controller.circle_pressed += self.o_handler
        self.controller.r2_changed += self.r2_handler
        self.controller.left_joystick_changed += self.joystick_handler
        self.controller.share_pressed += self.share_handler

        # if on windows, start dummy
        if os.name == "nt":
            self.rolling_basis = RollingBasisDummy(logger=self.logger)
            print("Dummy started")
        else:
            self.rolling_basis = RollingBasis(logger=self.logger)
            print("Rolling Basis started")

        while self.run:
            self.auto_handler()

    def stop(self):
        self.run = False
        self.controller.close()
        self.websocket = None

    def auto_handler(self):
        self.rolling_basis.set_speed(
            target_linear_speed=self.throttle,
            target_angular_speed=self.steering,
        )

    def joystick_handler(self, stateX, stateY):
        self.steering = -stateX / 128
        self.throttle = -stateY / 2

    def o_handler(self, state):
        if state == 1:
            self.stop()

    def r2_handler(self, state):
        # if state < self.deadzone:
        #     self.throttle = 0
        #     return
        # self.throttle = state
        return


if __name__ == "__main__":
    client = Client()
    client.start()
