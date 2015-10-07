import time
import pigpio
import sys

servos = 4 #GPIO number

pi = pigpio.pi()
#pulsewidth can only set between 500-2500

def correct_servo ():
        while True:
            pi.set_servo_pulsewidth(servos, 2500)
            time.sleep(.5)

            pi.set_servo_pulsewidth(servos, 1300)
            time.sleep(.5)

            pi.set_servo_pulsewidth(servos, 2500)
            time.sleep(.5)

            pi.set_servo_pulsewidth(servos, 1300)
            time.sleep(.5)

            pi.set_servo_pulsewidth(servos, 2500)
            time.sleep(.5)

            pi.set_servo_pulsewidth(servos, 1300)
            time.sleep(.5)

            pi.set_servo_pulsewidth(servos, 0);
            pi.stop()
            break

def incorrect_servo ():
    while True:
        pi.set_servo_pulsewidth(servos, 2500)
        time.sleep(.5)

        pi.set_servo_pulsewidth(servos, 1300)
        time.sleep(.5)

        pi.set_servo_pulsewidth(servos, 0);
        pi.stop()
        break

correct_servo()
incorrect_servo()
sys.exit
