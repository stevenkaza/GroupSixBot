import RPi.GPIO as GPIO  # Library for getting input from the line sensor
from RPIO import PWM  # Library for controlling the servos
import time  # used for sleeping between actions
import curses  # used for getting input from user, and displaying feedback
import sys  # used for exit of the program
​
## set which pins are operating the motors and the line sensor
left_motor = 17
right_motor = 27
line_sensor = 23
​
## Setup GPIO for reading the line sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(line_sensor, GPIO.IN)
​
## set up PWM for servos
servo = PWM.Servo()
​
​
## display kb input to console
def display_input(stdscr, kboutput):
    stdscr.clear()
    stdscr.addstr(kboutput)
    stdscr.refresh()
    stdscr.move(0, 0)
​
​
def kb_input(stdscr):
    ##default camera position
    state = 1500
    ##camera step difference
    step = 100
    k = 0n # used so we can keep an action happening until another key is pressed
    in_line_following = False
    try:
        stdscr.nodelay(1) # makes getch non blocking
        while True:
            ## get user input
            c = stdscr.getch()
            ## if no input and not in line following
            if (c != -1) and (in_line_following is False):
                if (c == 261) and (c != k):  # right key
                    k = c
                    turn_movement_servos(0, 80)  # turn wheels right
                    display_input(stdscr, "Right")
                elif (c == 260) and (c != k):  # left key turn left
                    k = c
                    turn_movement_servos(80, 0)
                    display_input(stdscr, "Left")
                elif (c == 259) and (c != k):  # up key turn forwards
                    k = c
                    turn_movement_servos(100, 100)
                    display_input(stdscr, "Forwards")
                elif (c == 258) and (c != k):  # down key turn backwards
                    k = c
                    turn_movement_servos(-100, -100)
                    display_input(stdscr, "Backwards")
                elif (c == 10) and (c != k):  # enter down key turn stop
                    k = c
                    turn_movement_servos(0, 0)
                    display_input(stdscr, "Stopped")
                elif (c == 113) and (c != k):  # quit script 'Q'
                    display_input(stdscr, "QUITING!")
                    time.sleep(0.5)
                    RPIO.cleanup()
                    sys.exit()
                elif (c == 32) and (c != k):  # switch to line following 'Space'
                    k = c
                    in_line_following = True
                    line_following()  # run line follower code
                    display_input(stdscr, "Line Following")
                elif c == 102 and (c != k):  # bring pen down
                    k = c
                    pen_movement("up")
                    display_input(stdscr, "Pen up")
                elif c == 100 and c != k:  # bring pen up
                    k = c
                    pen_movement("down")
                    display_input(stdscr, "Pen down")
                elif c == 101:  # camera up - 'E'
                    k = c
                    state = camera_movement("up", step, state)
                    display_input(stdscr, ("Camera up " + str(state)))
                elif c == 114:  # camera down - 'R'
                    k = c
                    state = camera_movement("down", step, state)
                    display_input(stdscr, ("Camera down " + str(state)))
                else:
                    if k != c:
                        d = "ASCII " + str(c) + " Value does nothing!"
                        display_input(stdscr, d)
            ## line following button actions
            elif c == 32:
                in_line_following = False
                stop()  # stop wheels turning
                display_input(stdscr, "Stopped")
            elif c == 113:
                display_input(stdscr, "QUITING!")
                time.sleep(0.5)
                RPIO.cleanup()
                sys.exit()
            else:
                if in_line_following:
                    line_following()  # run line follower code
                    display_input(stdscr, "Line Following")
​
    except curses.error:  # buttons held down for too long will throw an error in the curses library
        curses.wrapper(kbinput)  # so if that happens, just re-invoke the wrapper again
​
​
def turn_movement_servos(left_speed, right_speed):
    servo.set_servo(left_motor, 1520 + (-1 * left_speed))
    servo.set_servo(right_motor, 1520 + (1 * right_speed))

def clean_up():
	RPIO.cleanup()
    sys.exit()
​
​
def check_on_line():
    ## if sensor is low input, line is detected, else false
    if GPIO.input(line_sensor) == GPIO.LOW:
        on_line = True
    else:
        on_line = False
    return on_line
​
​
def line_following():  # simple line follow algorithm
    if check_on_line(): # if on_line turn left, else turn right, sleep for 0.1 secs
        turn_movement_servos(100, 40)
    else:
        turn_movement_servos(40, 100)
    time.sleep(0.1)
​
​
def pen_movement(position):
    if position == "up":
        servo.set_servo(pen_servo, 2200)  # set to the up position
    elif position == "down":
        servo.set_servo(pen_servo, 600)  # set to the down position
​
​
def camera_movement(direction, step, state):
    if direction is "up": # move camera up in increments based on the step
        if (state - step) > 650:
            state -= step
        elif (state - step) <= 650:
            state = 650
    elif direction is "down": # move camera down in increments based on the step
        if (state + step) < 2400:
            state += step
        elif (state + step) >= 2400:
            state = 2400
    servo.set_servo(camera_servo, state)  # set the servo and return the state of the servo
    return state
​
​
## main loop in this function
curses.wrapper(kb_input) # allows the terminal to return to a sane state after termination
