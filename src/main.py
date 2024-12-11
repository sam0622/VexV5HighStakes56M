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
from os import name

# Brain + Controller definition
brain: Brain = Brain()
controller_1: Controller = Controller()

# Motor configuration
drive_fr: Motor = Motor(Ports.PORT2, True)
drive_fl: Motor = Motor(Ports.PORT8, False)
drive_mr: Motor = Motor(Ports.PORT4, True)
drive_ml: Motor = Motor(Ports.PORT7, False)
drive_br: Motor = Motor(Ports.PORT5, True)
drive_bl: Motor = Motor(Ports.PORT6, False)
intake: Motor = Motor(Ports.PORT18, True)
conveyor: Motor = Motor(Ports.PORT9, True)
drive_motors_right: MotorGroup = MotorGroup(drive_fr, drive_mr, drive_br)
drive_motors_left: MotorGroup = MotorGroup(drive_fl, drive_ml, drive_bl)
intake.set_velocity(100, PERCENT)

# Pneumatics configuration
goal_lock: DigitalOut = DigitalOut(brain.three_wire_port.a)
goal_release: DigitalOut = DigitalOut(brain.three_wire_port.b)
# endregion

# region Auton Functions


def move_forward(time: float, speed: int = 100) -> None:
    drive_motors_right.spin(FORWARD, speed, PERCENT)
    drive_motors_left.spin(FORWARD, speed, PERCENT)
    sleep(time)
    drive_motors_right.stop()
    drive_motors_left.stop()


def move_backward(time: float, speed: int = 100) -> None:
    drive_motors_right.spin(REVERSE, speed, PERCENT)
    drive_motors_left.spin(REVERSE, speed, PERCENT)
    sleep(time)
    drive_motors_right.stop()
    drive_motors_left.stop()


def turn_right(time: float, speed: int = 100) -> None:
    drive_motors_right.spin(REVERSE, speed, PERCENT)
    drive_motors_left.spin(FORWARD, speed, PERCENT)
    sleep(time)
    drive_motors_right.stop()
    drive_motors_left.stop()


def turn_left(time: float, speed: int = 100) -> None:
    drive_motors_right.spin(FORWARD, speed, PERCENT)
    drive_motors_left.spin(REVERSE, speed, PERCENT)
    sleep(time)
    drive_motors_right.stop()
    drive_motors_left.stop()


# endregion

# region Callbacks


def controller_R1_pressed() -> None:
    conveyor.spin(FORWARD)
    while controller_1.buttonR1.pressing():
        wait(5, MSEC)
    conveyor.stop()


def controller_L1_pressed() -> None:
    conveyor.spin(REVERSE)
    while controller_1.buttonR1.pressing():
        wait(5, MSEC)
    conveyor.stop()


def controller_R2_pressed() -> None:
    intake.spin(FORWARD)
    while controller_1.buttonR2.pressing():
        wait(5, MSEC)
    intake.stop()


def controller_L2_pressed() -> None:
    intake.spin(REVERSE)
    while controller_1.buttonL2.pressing():
        wait(5, MSEC)
    intake.stop()


def controller_A_pressed() -> None:
    if goal_lock.value() == 0:
        goal_lock.set(True)
        goal_release.set(False)
    else:
        goal_lock.set(False)
        goal_release.set(True)


controller_1.buttonR1.pressed(controller_R1_pressed)
controller_1.buttonL1.pressed(controller_L1_pressed)
controller_1.buttonR2.pressed(controller_R2_pressed)
controller_1.buttonL2.pressed(controller_L2_pressed)
controller_1.buttonA.pressed(controller_A_pressed)
wait(15, MSEC)
# endregion

# region Control

intake.set_velocity(100, PERCENT)


def drive_task() -> None:
    while True:

        # Motor control
        drive_motors_right.spin(FORWARD)
        drive_motors_left.spin(FORWARD)

        drive_motors_right.set_velocity(controller_1.axis2.position(), PERCENT)
        drive_motors_left.set_velocity(controller_1.axis3.position(), PERCENT)

        wait(5, MSEC)


def pre_autonomous() -> None:
    pass


def autonomous() -> None:
    pass


def user_control() -> None:
    drive_thread: Thread = Thread(drive_task)


# endregion
