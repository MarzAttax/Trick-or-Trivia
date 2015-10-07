from Tkinter import *
import RPi.GPIO as GPIO
import time
import sys
import pygame
import pigpio


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

servos = 4 #GPIO number
pi = pigpio.pi()

state = True

correct_audio_path = '/home/pi/Desktop/audio/correct.mp3'
incorrect_audio_path = '/home/pi/Desktop/audio/incorrect.mp3'

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


def blink_led():
    # endless loop, on/off for 1 second
    while True:
        GPIO.output(26,True)
        pygame.mixer.init()
        pygame.mixer.music.load(correct_audio_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(5)
        time.sleep(10)
        correct_servo()
        GPIO.output(26,False)
        GPIO.cleanup()
        pygame.quit()
        sys.exit()

def blink_led_2():
    # endless loop, on/off for 1 second
    while True:
        GPIO.output(19, True)
        pygame.mixer.init()
        pygame.mixer.music.load(incorrect_audio_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(5)
        time.sleep(10)
        incorrect_servo()
        GPIO.output(19,False)
        GPIO.cleanup()
        pygame.quit()
        sys.exit()




root = Tk()
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.focus_set()  # <-- move focus to this widget
root.configure(background='black')

label_1 = Label(root, text="Welcome to Trick or Trivia", font=("Helvetica", 36), bg="black", fg="white")
label_1.grid(columnspan=6,padx=(100, 10))
label_2 = Label(root, text="Answer the question for candy!", font=("Helvetica", 28), bg="black", fg="red")
label_2.grid(columnspan=6, pady=5, padx=(100, 10))

label_3 = Label(root, text="Casper is a friendly ____!", font=("Helvetica", 32), bg="black", fg="green")
label_3.grid(columnspan=6, pady=5, padx=(100, 10))

button_1 = Button(root, text="Ghost", font=("Helvetica", 36), command=blink_led)
button_1.grid(row=4, column=2, pady=5, padx=(100, 10))


button_2 = Button(root, text="Ghast", font=("Helvetica", 36), command=blink_led_2)
button_2.grid(row=4, column=4, sticky=W, padx=(100, 10))

button_3 = Button(root, text="Ghoul", font=("Helvetica", 36), command=blink_led_2)
button_3.grid(row=5, column=2, pady=5, padx=(100, 10))

button_4 = Button(root, text="Gremlin", font=("Helvetica", 36), command=blink_led_2)
button_4.grid(row=5, column=4, sticky=W, padx=(100, 10))

label_4 = Label(root, text="Correct Answer = 3 Pieces", font=("Helvetica", 20), bg="black", fg="green")
label_4.grid(columnspan=6, padx=(100, 10))

label_5 = Label(root, text="Incorrect Answer = 1 Piece", font=("Helvetica", 20), bg="black", fg="red")
label_5.grid(columnspan=6, padx=(100, 10))


root.mainloop()
