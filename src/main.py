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
top_left: Motor = Motor(Ports.PORT18, False, GearSetting.RATIO_6_1)
bottom_left: Motor = Motor(Ports.PORT17, True, GearSetting.RATIO_6_1)
back_left: Motor = Motor(Ports.PORT16, True, GearSetting.RATIO_6_1)
top_right: Motor = Motor(Ports.PORT8, False, GearSetting.RATIO_6_1)
bottom_right: Motor = Motor(Ports.PORT9, True, GearSetting.RATIO_6_1)
back_right: Motor = Motor(Ports.PORT10, False, GearSetting.RATIO_6_1)
conveyor: Motor = Motor(Ports.PORT20, False, GearSetting.RATIO_18_1)
intake: Motor = Motor(Ports.PORT19, False, GearSetting.RATIO_18_1)
left_group: MotorGroup = MotorGroup(top_left, bottom_left, back_left)
right_group: MotorGroup = MotorGroup(top_right, bottom_right, back_right)


# Pneumatics configuration
goal_solenoid: DigitalOut = DigitalOut(brain.three_wire_port.a)
goal_solenoid.set(True)

# Global variables
precision_mode: bool = False


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
    right_group.spin(REVERSE, speed, PERCENT)
    left_group.spin(FORWARD, speed, PERCENT)
    sleep(time, SECONDS)
    right_group.stop()
    left_group.stop()


def turn_left(time: float, speed: int = 100) -> None:
    right_group.spin(FORWARD, speed, PERCENT)
    left_group.spin(REVERSE, speed, PERCENT)
    sleep(time, SECONDS)
    right_group.stop()
    left_group.stop()


def intake_and_conveyor(time: float) -> None:
    intake.spin(FORWARD)
    conveyor.spin(FORWARD)
    sleep(time, SECONDS)
    intake.stop()
    conveyor.stop()


def convey(time: float) -> None:
    conveyor.spin(FORWARD)
    sleep(time, SECONDS)
    conveyor.stop()


def clamp_goal() -> None:
    if goal_solenoid.value() == 0:
        goal_solenoid.set(1)
    else:
        goal_solenoid.set(0)
    print(goal_solenoid.value())


# endregion

# region Callbacks


def controller_R1_pressed() -> None:
    conveyor.spin(FORWARD)
    while controller_1.buttonR1.pressing():
        wait(5, MSEC)
    conveyor.stop()


def controller_L1_pressed() -> None:
    conveyor.spin(REVERSE)
    while controller_1.buttonL1.pressing():
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
    clamp_goal()


def controller_up_pressed() -> None:
    global precision_mode
    precision_mode = not precision_mode
    if precision_mode:
        controller_1.rumble(".")
    else:
        controller_1.rumble("-")


controller_1.buttonR1.pressed(controller_R1_pressed)
controller_1.buttonL1.pressed(controller_L1_pressed)
controller_1.buttonR2.pressed(controller_R2_pressed)
controller_1.buttonL2.pressed(controller_L2_pressed)
controller_1.buttonA.pressed(controller_A_pressed)
controller_1.buttonUp.pressed(controller_up_pressed)

wait(15, MSEC)
# endregion

# region Control


def driver_control() -> None:
    return
    while True:
        right_group.spin(FORWARD)
        left_group.spin(FORWARD)
        if precision_mode:
            right_group.set_velocity(controller_1.axis2.position() * 0.5, PERCENT)
            left_group.set_velocity(controller_1.axis3.position() * 0.5, PERCENT)
        else:
            right_group.set_velocity(controller_1.axis2.position(), PERCENT)
            left_group.set_velocity(controller_1.axis3.position(), PERCENT)
        wait(5, MSEC)


def pre_autonomous() -> None:
    global precision_mode
    precision_mode = False
    conveyor.set_velocity(75, PERCENT)
    intake.set_velocity(100, PERCENT)
    goal_solenoid.set(0)


def autonomous() -> None:
    goal_solenoid.set(0)
    move_backward(0.5, 50)
    turn_left(0.5, 50)
    move_forward(1, 50)
    clamp_goal()
    clamp_goal()
    clamp_goal()
    convey(1)  


def user_control() -> None:
    driver_control()


pre_autonomous()
comp: Competition = Competition(autonomous, user_control)
# endregion
