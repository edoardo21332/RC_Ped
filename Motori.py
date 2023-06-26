import RPi.GPIO as GPIO  # Importing the GPIO library for controlling the pins on the Raspberry Pi
import serial  # Importing the serial library for serial communication
from time import sleep  # Importing the sleep function from the time module
#import test.ProvaEncoder as ProvaEncoder
import time


uart_channel = serial.Serial("/dev/ttyAMA0", baudrate=38400, timeout=2)  # Setting up the serial channel for communication with a device
data1 = ""  # Initializing an empty string variable
data = b''  # Initializing an empty bytes variable


GPIO.setmode(GPIO.BCM)  # Setting the pin numbering mode to BCM
GPIO.setwarnings(False)  # Disabling the GPIO warnings

# Defining the pins used for controlling the motors
IN1 = 12
IN2 = 21
IN3 = 13
IN4 = 11
PIN_ENCODER = 26
PIN_ENCODER_2 = 20

pwmdx = 40
pwmsx = 40


# Setting up the pins for motor control as output pins
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(PIN_ENCODER, GPIO.IN)
GPIO.setup(PIN_ENCODER_2, GPIO.IN)

# Setting up PWM channels for controlling the speed of the motors
PWMA = GPIO.PWM(IN2, 100)
PWMA.start(0)
PWMB = GPIO.PWM(IN4, 100)
PWMB.start(0)


def straight():
    """Function for moving the robot forward"""
    flag = True
    while True:
        if flag:
            GPIO.output(IN1, GPIO.LOW)
            PWMB.ChangeDutyCycle(pwmdx)
            GPIO.output(IN3, GPIO.LOW)
            PWMA.ChangeDutyCycle(pwmsx)  # Turning right from the front
            flag = engineInMotion_Motor_1()
        else:
          break
        GPIO.output(IN1, GPIO.LOW)
        PWMB.ChangeDutyCycle(0)
        GPIO.output(IN3, GPIO.LOW)
        PWMA.ChangeDutyCycle(0)
        


def engineInMotion_Motor_1():
    """check if the engine is moving"""
    oldValue=GPIO.input(PIN_ENCODER)

    t0 = time.time()
    impulsi=0
    while time.time() - t0 < 0.05:
            newValue=GPIO.input(PIN_ENCODER)          
            if (oldValue==0 and newValue==1 ):
                impulsi = impulsi + 1
            oldValue=newValue

    if impulsi==0:
        return False

    else :
        return True

def engineInMotion_Motor_2():
    """check if the engine is moving"""
    oldValue2 = GPIO.input(PIN_ENCODER_2)
    t0 = time.time()
    impulsi=0
    while time.time() - t0 < 0.05:
            newValue2=GPIO.input(PIN_ENCODER_2)
            if (oldValue2==0 and newValue2==1):
                impulsi = impulsi + 1
            oldValue2=newValue2

    if impulsi==0:
        return False

    else :
        return True


def straightTime(tempo):
    """Function for moving the robot forward for a given time"""
    t0 = time.time()
    flag_Motor_1 = True
    flag_Motor_2 = True
    GPIO.output(IN1, GPIO.LOW)
    PWMB.ChangeDutyCycle(pwmdx)
    GPIO.output(IN3, GPIO.LOW)
    PWMA.ChangeDutyCycle(pwmsx)  # Turning right from the front
    while time.time() - t0 < tempo or flag_Motor_1 or flag_Motor_2:
        flag_Motor_1 = engineInMotion_Motor_1()
        flag_Motor_2 = engineInMotion_Motor_2
        print(flag_Motor_1)
        print(flag_Motor_2)
    GPIO.output(IN1, GPIO.LOW)
    PWMB.ChangeDutyCycle(0)
    GPIO.output(IN3, GPIO.LOW)
    PWMA.ChangeDutyCycle(0)


def right(tempo):
    """Function for turning the robot right"""
    t0 = time.time()
    flag = True
    GPIO.output(IN1, GPIO.LOW)
    PWMB.ChangeDutyCycle(pwmsx)
    GPIO.output(IN3, GPIO.LOW)
    PWMA.ChangeDutyCycle(0)  # Turning right from the front
    while time.time() - t0 < tempo or flag:
        flag = engineInMotion_Motor_1()
        print(flag)
    GPIO.output(IN1, GPIO.LOW)
    PWMB.ChangeDutyCycle(0)
    GPIO.output(IN3, GPIO.LOW)
    PWMA.ChangeDutyCycle(0)

def left(tempo):
    """Function for turning the robot left"""
    t0 = time.time()
    flag = True
    GPIO.output(IN1, GPIO.LOW)
    PWMB.ChangeDutyCycle(0)
    GPIO.output(IN3, GPIO.LOW)
    PWMA.ChangeDutyCycle(pwmdx)  # Turning right from the front
    while time.time() - t0 < tempo or flag:
        flag = engineInMotion_Motor_2()
        print(flag)
    GPIO.output(IN1, GPIO.LOW)
    PWMB.ChangeDutyCycle(0)
    GPIO.output(IN3, GPIO.LOW)
    PWMA.ChangeDutyCycle(0)


def stop():
    """Function for stopping the robot"""
    GPIO.output(IN1,GPIO.LOW)
    PWMA.ChangeDutyCycle(0)
    GPIO.output(IN3,GPIO.LOW)
    PWMB.ChangeDutyCycle(0)
