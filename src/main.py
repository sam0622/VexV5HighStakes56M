# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       samuel.greenfield                                            #
# 	Created:      9/4/2024, 1:07:23 PM                                         #
# 	Description:  Code for Vex V5 High Stakes                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

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

# Vision configuration
BLUE_RING: Signature = Signature(1, -5535, -4895, -5214,2881, 4879, 3880,4.5, 0)
RED_RING: Signature = Signature(0, 0, 0, 0, 0, 0, 0, 0, 0)
vision_sensor: Vision = Vision(Ports.PORT15, 50, BLUE_RING, RED_RING)

#-----------------#
# Auton functions #
#-----------------#

def move_forward(time: float, speed: int=100) -> None:
    drive_motors_right.spin(FORWARD, speed, PERCENT)
    drive_motors_left.spin(FORWARD, speed, PERCENT)
    sleep(time)
    drive_motors_right.stop()
    drive_motors_left.stop()

def move_backward(time: float, speed: int=100) -> None:
    drive_motors_right.spin(REVERSE, speed, PERCENT)
    drive_motors_left.spin(REVERSE, speed, PERCENT)
    sleep(time)
    drive_motors_right.stop()
    drive_motors_left.stop()

def turn_right(time: float, speed: int=100) -> None:
    drive_motors_right.spin(REVERSE, speed, PERCENT)
    drive_motors_left.spin(FORWARD, speed, PERCENT)
    sleep(time)
    drive_motors_right.stop()
    drive_motors_left.stop()

def turn_left(time: float, speed: int=100) -> None:
    drive_motors_right.spin(FORWARD, speed, PERCENT)
    drive_motors_left.spin(REVERSE, speed, PERCENT)
    sleep(time)
    drive_motors_right.stop()
    drive_motors_left.stop()

#------------------#
# Button callbacks #
#------------------#

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

controller_1.buttonR1.pressed(controller_R1_pressed)
controller_1.buttonL1.pressed(controller_L1_pressed)
controller_1.buttonR2.pressed(controller_R2_pressed)
controller_1.buttonL2.pressed(controller_L2_pressed)
wait(15, MSEC)

# Main driving thread
intake.set_velocity(100, PERCENT)
def drive_task() -> None:

    while True:

        # Motor control
        drive_motors_right.spin(FORWARD)
        drive_motors_left.spin(FORWARD)

        drive_motors_right.set_velocity(controller_1.axis2.position(), PERCENT)
        drive_motors_left.set_velocity(controller_1.axis3.position(), PERCENT)
        
        wait(5, MSEC)

# Processing for vision sensor
def vision_processing() -> None:
    pass

def pre_autonomous() -> None:
    pass

def autonomous() -> None:
    pass

def user_control() -> None:
    drive_thread: Thread = Thread(drive_task)
    vision_thread: Thread = Thread(vision_processing)