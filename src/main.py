# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       samuel.greenfield                                            #
# 	Created:      9/4/2024, 1:07:23 PM                                         #
# 	Description:  Code for Vex V5 High Stakes                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# region Configuration

# Library imports
from vex import *

# Brain + Controller definition
brain: Brain = Brain()
controller_1: Controller = Controller()

# Motor configuration
top_left: Motor = Motor(Ports.PORT18, True, GearSetting.RATIO_6_1)
bottom_left: Motor = Motor(Ports.PORT17, False, GearSetting.RATIO_6_1)
back_left: Motor = Motor(Ports.PORT16, False, GearSetting.RATIO_6_1)
top_right: Motor = Motor(Ports.PORT10, False, GearSetting.RATIO_6_1)
bottom_right: Motor = Motor(Ports.PORT9, True, GearSetting.RATIO_6_1)
back_right: Motor = Motor(Ports.PORT8, True, GearSetting.RATIO_6_1)

left_group: MotorGroup = MotorGroup(top_left, bottom_left, back_left)
right_group: MotorGroup = MotorGroup(top_right, bottom_right, back_right)


# Pneumatics configuration
goal_solenoid: DigitalOut = DigitalOut(brain.three_wire_port.a)

# endregion

# region Auton Functions


def move_forward(time: float, speed: int = 100) -> None:
    right_group.spin(FORWARD, speed, PERCENT)
    left_group.spin(FORWARD, speed, PERCENT)
    sleep(time, SECONDS)
    right_group.stop()
    left_group.stop()


def move_backward(time: float, speed: int = 100) -> None:
    right_group.spin(REVERSE, speed, PERCENT)
    left_group.spin(REVERSE, speed, PERCENT)
    sleep(time, SECONDS)
    right_group.stop()
    left_group.stop()


def turn_right(time: float, speed: int = 100) -> None:
    right_group.spin(FORWARD, speed, PERCENT)
    left_group.spin(REVERSE, speed, PERCENT)
    sleep(time, SECONDS)
    right_group.stop()
    left_group.stop()


def turn_left(time: float, speed: int = 100) -> None:
    right_group.spin(REVERSE, speed, PERCENT)
    left_group.spin(FORWARD, speed, PERCENT)
    sleep(time, SECONDS)
    right_group.stop()
    left_group.stop()


def intake_and_conveyer(time: float) -> None:
    # intake.spin(FORWARD)
    # conveyor.spin(FORWARD)
    sleep(time, SECONDS)
    # intake.stop()
    # conveyor.stop()


# def clamp_goal() -> None:
#   if goal_solenoid.value() == 0:
# goal_solenoid.set(True)
#  else:
# goal_solenoid.set(False)


# endregion

# region Callbacks


def controller_R1_pressed() -> None:
    # conveyor.spin(FORWARD)
    while controller_1.buttonR1.pressing():
        wait(5, MSEC)
    # conveyor.stop()


def controller_L1_pressed() -> None:
    # conveyor.spin(REVERSE)
    while controller_1.buttonL1.pressing():
        wait(5, MSEC)
    # conveyor.stop()


def controller_R2_pressed() -> None:
    # intake.spin(FORWARD)
    while controller_1.buttonR2.pressing():
        wait(5, MSEC)
    # intake.stop()


def controller_L2_pressed() -> None:
    # intake.spin(REVERSE)
    while controller_1.buttonL2.pressing():
        wait(5, MSEC)
    # intake.stop()


def controller_A_pressed() -> None:
    # clamp_goal()
    pass


controller_1.buttonR1.pressed(controller_R1_pressed)
controller_1.buttonL1.pressed(controller_L1_pressed)
controller_1.buttonR2.pressed(controller_R2_pressed)
controller_1.buttonL2.pressed(controller_L2_pressed)
controller_1.buttonA.pressed(controller_A_pressed)

wait(15, MSEC)
# endregion

# region Control


def driver_control() -> None:
    while True:
        # Motor control
        right_group.spin(FORWARD)
        left_group.spin(FORWARD)

        right_group.set_velocity(controller_1.axis2.position(), PERCENT)
        left_group.set_velocity(controller_1.axis3.position(), PERCENT)
        print(left_group.velocity(PERCENT), right_group.velocity(PERCENT))

        wait(5, MSEC)


def pre_autonomous() -> None:
    # conveyor.set_velocity(75, PERCENT)
    # intake.set_velocity(100, PERCENT)
    # goal_solenoid.set(0)
    pass


def autonomous() -> None:
    pass


def user_control() -> None:
    driver_control()


comp: Competition = Competition(user_control, autonomous)
pre_autonomous()

# endregion
