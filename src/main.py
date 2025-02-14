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
lady_brown: Motor = Motor(Ports.PORT7, True, GearSetting.RATIO_18_1)
left_group: MotorGroup = MotorGroup(top_left, bottom_left, back_left)
right_group: MotorGroup = MotorGroup(top_right, bottom_right, back_right)
motors: MotorGroup = MotorGroup(
    top_left,
    bottom_left,
    back_left,
    top_right,
    bottom_right,
    back_right,
    conveyor,
    intake,
    lady_brown,
)


# Pneumatics configuration
goal_solenoid: DigitalOut = DigitalOut(brain.three_wire_port.a)
goal_solenoid.set(True)

# Button
button: DigitalIn = DigitalIn(brain.three_wire_port.b)

# Global variables
precision_mode: bool = False
offense: bool = True

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


def intake_and_conveyor(time: float, speed: int = 100, reverse: bool = False) -> None:
    if reverse:
        intake.spin(REVERSE)
        conveyor.spin(REVERSE)
    else:
        intake.spin(FORWARD)
        conveyor.spin(FORWARD)
    sleep(time, SECONDS)
    intake.stop()
    conveyor.stop()


def eat_and_run(time: float, speed: int = 100) -> None:
    intake.spin(FORWARD)
    right_group.spin(REVERSE, speed, PERCENT)
    left_group.spin(REVERSE, speed, PERCENT)
    conveyor.set_velocity(75, PERCENT)
    conveyor.spin(FORWARD)
    sleep(time, SECONDS)
    right_group.stop()
    left_group.stop()
    sleep(0.9, SECONDS)
    intake.stop()
    conveyor.stop()


def convey(time: float, reverse: bool = False) -> None:
    if reverse:
        conveyor.spin(REVERSE)
    else:
        conveyor.spin(FORWARD)
    sleep(time, SECONDS)
    conveyor.stop()


def mr_aneskos_cat(time: float, reverse: bool = False) -> None:
    lady_brown.set_velocity(100, PERCENT)
    if reverse:
        lady_brown.spin(REVERSE)
    else:
        lady_brown.spin(FORWARD)
    sleep(time, SECONDS)
    lady_brown.stop()


def thug_shaker() -> None:
    for i in range(2):
            move_forward(0.1)
            move_backward(0.1)


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


def controller_up_pressed() -> None:
    global precision_mode
    precision_mode = not precision_mode
    if precision_mode:
        controller_1.rumble(".")
    else:
        controller_1.rumble("-")


def controller_A_pressed() -> None:
    clamp_goal()


def controller_left_pressed() -> None:
    lady_brown.spin(REVERSE, 100, PERCENT)
    while controller_1.buttonLeft.pressing():
        wait(5, MSEC)
    lady_brown.stop()


def controller_right_pressed() -> None:
    lady_brown.spin(FORWARD, 100, PERCENT)
    while controller_1.buttonRight.pressing():
        wait(5, MSEC)
    lady_brown.stop()

def controller_down_pressed() -> None:
    lady_brown.spin_to_position(-12, DEGREES, 100, PERCENT)


controller_1.buttonR1.pressed(controller_R1_pressed)
controller_1.buttonL1.pressed(controller_L1_pressed)
controller_1.buttonR2.pressed(controller_R2_pressed)
controller_1.buttonL2.pressed(controller_L2_pressed)
controller_1.buttonA.pressed(controller_A_pressed)
controller_1.buttonUp.pressed(controller_up_pressed)
controller_1.buttonLeft.pressed(controller_left_pressed)
controller_1.buttonRight.pressed(controller_right_pressed)
controller_1.buttonDown.pressed(controller_down_pressed)

wait(15, MSEC)
# endregion

# region Control


def user_control() -> None:
    while True:
        if lady_brown.position() > 0:
            lady_brown.spin_to_position(0, DEGREES, 100, PERCENT)
        elif lady_brown.position() < -975:
            lady_brown.spin_to_position(-975, DEGREES, 100, PERCENT)
        print(lady_brown.position(), lady_brown.temperature())
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
    global precision_mode, offense
    precision_mode = False
    motors.set_stopping(HOLD)
    conveyor.set_velocity(75, PERCENT)
    intake.set_velocity(100, PERCENT)
    goal_solenoid.set(0)
    previous: int = button.value()
    controller_1.screen.print("Offense")
    while True:
        print(button.value(), offense)
        if button.value() == 1 and previous == 0:
            previous = 1
            offense = not offense
            if offense:
                controller_1.screen.clear_line(1)
                controller_1.screen.set_cursor(0, 1)
                controller_1.screen.print("Offense")
            else:
                controller_1.screen.clear_line(1)
                controller_1.screen.set_cursor(0, 1)
                controller_1.screen.print("Defense")

            wait(500, MSEC)

        elif button.value() == 0:
            previous = 0
        wait(5, MSEC)

        if Competition.is_enabled():
            break


def autonomous() -> None:
    global offense
    if offense:
        mr_aneskos_cat(0.4, True)
        move_forward(0.65, 75)  
        clamp_goal()
        thug_shaker()
        convey(1.5)
        thug_shaker()
        for i in range(2):
            convey(0.5, True)
            convey(0.5)
        turn_right(0.3)   
        eat_and_run(1.25, 50)   
        convey(1)
        thug_shaker()
        for i in range(2):
            convey(0.5, True)
            convey(0.5)
        move_forward(2, 50)
    else:
        mr_aneskos_cat(0.4, True)
        move_forward(0.65, 75)  
        clamp_goal()
        thug_shaker()
        convey(1.5)
        thug_shaker()
        for i in range(2):
            convey(0.5, True)
            convey(0.5)
        turn_left(0.3)   
        eat_and_run(1.25, 50)   
        convey(1)
        thug_shaker()
        for i in range(2):
            convey(0.5, True)
            convey(0.5)
        move_forward(2, 50)


#limiter: Thread = Thread(position_limiter)
pre_autonomous()
comp: Competition = Competition(user_control, autonomous)
# endregion
