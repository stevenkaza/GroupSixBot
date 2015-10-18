import RPi.GPIO as GPIO  # Library for getting input from the line sensor
import time  # used for sleeping between actions
import curses  # used for getting input from user, and displaying feedback
import sys  # used for exit of the program
## set which pins are operating the motors and the line sensor
left_motor = 17
right_motor = 27
line_sensor = 23
def turn_movement_servos(left_speed, right_speed):
    servo.set_servo(left_motor, 1520 + (-1 * left_speed))
    servo.set_servo(right_motor, 1520 + (1 * right_speed))


turn_movement_servos(80,100)
