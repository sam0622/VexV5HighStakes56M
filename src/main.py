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
drive_fl: Motor = Motor(Ports.PORT11, False)
drive_ml: Motor = Motor(Ports.PORT12, False)
drive_bl: Motor = Motor(Ports.PORT13, False)
drive_fr: Motor = Motor(Ports.PORT16, True)
drive_mr: Motor = Motor(Ports.PORT17, False)
drive_br: Motor = Motor(Ports.PORT18, True)
conveyor: Motor = Motor(Ports.PORT10, True)
intake: Motor = Motor(Ports.PORT9, True)

drive_motors_right: MotorGroup = MotorGroup(drive_fr, drive_mr, drive_br)
drive_motors_left: MotorGroup = MotorGroup(drive_fl, drive_ml, drive_bl)
conveyor.set_velocity(100, PERCENT)
intake.set_velocity(100, PERCENT)

# Pneumatics configuration
goal_solenoid: DigitalOut = DigitalOut(brain.three_wire_port.a)
goal_solenoid.set(1)
# Auton conditions
is_defense: bool = True
is_auton: bool = True
is_pre_auton: bool = True
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
    switch_goal_lock()


def controller_B_pressed() -> None:
    global is_auton, is_pre_auton, is_defense
    if is_auton and is_pre_auton:
        controller_1.rumble(".--")
        if is_defense:
            is_defense = False
            controller_1.screen.clear_screen()
            controller_1.screen.print("Offense")
        else:
            controller_1.screen.clear_screen()
            controller_1.screen.print("Defense")
            is_defense = True
    else:
        controller_1.rumble(".")


controller_1.buttonR1.pressed(controller_R1_pressed)
controller_1.buttonL1.pressed(controller_L1_pressed)
controller_1.buttonR2.pressed(controller_R2_pressed)
controller_1.buttonL2.pressed(controller_L2_pressed)
controller_1.buttonA.pressed(controller_A_pressed)
controller_1.buttonB.pressed(controller_B_pressed)

wait(15, MSEC)
# endregion

# region Control

intake.set_velocity(100, PERCENT)


def switch_goal_lock() -> None:
    if goal_solenoid.value() == 0:
        goal_solenoid.set(True)
    else:
        goal_solenoid.set(False)


def drive_task() -> None:
    global is_auton, is_pre_auton
    while True:
        is_auton, is_pre_auton = False, False
        
        # Motor control
        drive_motors_right.spin(FORWARD)
        drive_motors_left.spin(FORWARD)

        drive_motors_right.set_velocity(controller_1.axis2.position(), PERCENT)
        drive_motors_left.set_velocity(controller_1.axis3.position(), PERCENT)
        print(drive_motors_left.velocity(PERCENT), drive_motors_right.velocity(PERCENT))

        wait(5, MSEC)


def pre_autonomous() -> None:
    global is_auton, is_pre_auton
    is_auton, is_pre_auton  = True, True
    controller_1.screen.print("Defense")
    pass


def autonomous() -> None:
    global is_auton, is_defense
    is_auton, is_pre_auton = True, False
    if is_defense:
        pass
    else:
        pass


def user_control() -> None:
    is_auton, is_pre_auton = False, False
    drive_task()


comp: Competition = Competition(user_control, autonomous)
pre_autonomous()

# endregion
