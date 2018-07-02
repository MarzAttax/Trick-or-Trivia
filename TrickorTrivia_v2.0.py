# Set the platform you are running on, comment out the rest.

# PLATFORM = "RPI"
PLATFORM = "LINUX"
# PLATFORM = "PC"
# PLATFORM = "MAC"


if (PLATFORM == "RPI"):
    import RPi.GPIO as GPIO  # import to enable GPIO commands

    correct_audio_path = '/home/pi/Desktop/Projects/ToT/audio/correct.mp3'
    incorrect_audio_path = '/home/pi/Desktop/Projects/ToT/audio/incorrect.mp3'
    game_open = '/home/pi/Desktop/Projects/ToT/audio/What is my purpose.mp3'

elif (PLATFORM == "LINUX"):
    # Replace libraries with fake ones
    import sys
    import fake_rpi

    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi (GPIO)
    sys.modules['smbus'] = fake_rpi.smbus  # Fake smbus (I2C)
    GPIO = fake_rpi.RPi.GPIO

    correct_audio_path = '/home/kristian/Projects/Trick-or-Trivia/cow.mp3'
    incorrect_audio_path = '/home/kristian/Projects/Trick-or-Trivia/cow.mp3'
    game_open = '/home/kristian/Projects/Trick-or-Trivia/cow.mp3'

elif (PLATFORM == "PC"):
    print("NOT TESTED!")

elif (PLATFORM == "MAC"):
    print("NOT TESTED!")

from tkinter import *  # import tkinter library for GUI, from shortens function calls
import time  # used for sleep commands
import sys  # if you used an exit option, you would need this
import pygame  # used to play audio
from pygame.locals import *  # not sure what this was used for
from random import randint  # a random number is used to select a random quiz

##GPIO.setwarnings(False)       # I don't think this is necessary if GPIO is cleaned upon exit/crash


# question, choice1, choice2, chioce3, choice4, correct answer, difficulty [difficulty][selection][data]
# EASY
quiz = [[["Casper is a friendly ____!", "Ghost", "Ghast", "Ghoul", "Gremlin", 1],
         ["Dracula is a _______.", "Snake", "Zombie", "Vampire", "pokemon", 3],
         ["Put a light in the _______ \nto light up its face.", "window", "pumpkin", "doorway", "refrigerator", 2],
         ["Witches love to fly around \non a _____.", "vacuum cleaner", "jet plane", "dragon", "broomstick", 4],
         ["Halloween is on which day?", "Oct 13", "Oct 31", "Nov 1", "Abc 45", 2],
         ["A _______ costume is scary \nbecause he wears fangs.", "robot", "mighty mouse", "vampire", "turkey", 3],
         ["To make a Jack o'Lantern  \nyou carve a ______.", "pumpkin", "birthday cake", "carrot", "watermellon", 1],
         ["Kids love to get _____ when \nthey go trick or treating!", "Fruit", "Cereal", "Kittens", "Candy", 4],
         ["What room do ghosts avoid?", "bathroom", "kitchen", "living room", "closet", 3]],  # end Easy

        # MEDIUM
        [["Pumpkins are a: ", "fruit", "vegetable", "mineral", "arthropod", 1],
         ["Who is the avid believer \nin the great pumpkin?", "Lucy", "Linus", "Charlie Brown", "John Cena!", 2],
         ["Which Disney princess rode \nto the ball in a pumpkin?", "Tianna", "Cinderella", "Snow White", "Shrek", 2],
         ["Every Halloween, Charlie Brown helps his \nfriend Linus wait for what character to appear?", "The Great Pumpkin", "Dracula", "Snoopy", "Pikachu", 1],
         ["How do pumpkins grow?", "on vines", "under ground", "in a bush", "in a tree", 1],
         ["Which country celebrates the Day of the \nDead starting at midnight on Oct. 31?", "China", "Canada", "America", "Mexico", 4],
         ["Pumpkins can be orange, white, green, or what other color?", "Purple", "Lavendar", "Black", "Blue", 4],
         ["Complete the following chant, normally said \nby witches: double, double, toil and …?", "Rubble", "Bubble", "Stubble", "Trouble", 4],
         ["What type of vegetable is disliked by \nvampires and is used to frighten them away?", "Carrots", "Ginger", "Garlic", "Salt", 3]],  # end Medium

        # HARD
        [["Pumpkins are made up of \nhow much water?", " 30% ", " 50% ", " 90% ", " OVER 9000% ", 3],
         ["The largest pumpkin ever \ngrown weighed how much?", "844 lbs", "1,140 lbs", "2,091 lbs", "3,000,000 lbs ", 3],
         ["Pumpkins contain \nsignificant amounts of: ", "potassium and Vit A", "magnesium and Vit C", "folate and Vit D", "free shavacado", 1],
         ["What variety is the \ntraditional Halloween pumpkin?", "Autumn Gold", "Conneticut Field", "Baby Boo", "Orange", 2],
         ["Pumpkins are grown on \nhow many continents?", "2", "5", "6", "9", 3],
         ["The first Jack-o-Lanterns \nwere made out of what?", "Watermelons", "Cantaloupe", "Turnips", "Pumpkins", 3],
         ["The average American household \nspends how much on Halloween candy?", "$28", "$35", "$44", "$52", 3],
         ["Where did Halloween originate?", "England", "America", "Scotland", "Ireland", 4],
         ["Which is the top-selling \ncandy for Halloween?", "Snickers", "Candy Corn", "M&Ms", "Reese's", 2],
         ["Which day of the year \nhas the highest candy sales?", "Oct 28th", "Oct 29th", "Oct 30th", "Oct 31st", 1],
         ["Of the $1.9 billion in candy sales, how \nmuch of it is from chocolate candy?", "$1 billion", "$1.2 billion", "$1.5 billion", "$1.7 billion", 2],
         ["The days leading up to Halloween account \nfor what % of the year's candy sales?", " 10% ", " 15% ", " 20% ", " 23% ", 1],
         ["What does the English \nword HALLOW mean?", "Sin", "Spirit", "Saint", "Spook", 3],
         ["What phobia do you suffer from if you \nhave an intense fear of Halloween?", "Phasmophobia", "Samhainophobia", "Wiccaphobia", "Halloweenphobia", 2],
         ["Halloween, the movie was \nmade in 1978 on a low \nbudget in how many days?", "12 days", "21 days", "30 days", "35 days", 2],
         ["According to legend, a unibrow, tattoos, \nand a long middle finger, are signs \nof which Halloween creature?", "Werewolf", "Witch", "Vampire", "Golem", 1],
         ["Which celebrity does not \nhave a Halloween Birthday?", "Vanilla Ice", "Dan Rather", "Peter Jackson", "Kevin Bacon", 4]]  # end Hard
        ]  # end quiz[]


class App(Frame):

    # init is run on object creation
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.playSound(game_open)  # This will play as soon as the app is started

    # This re-prints the header, it's called before each question is printed
    def header(self):
        self.label_1 = Label(root, text="Welcome to Trick or Trivia", font=("Helvetica", 36), bg="black", fg="white")
        self.label_1.grid(columnspan=6, padx=(100, 10))
        self.label_2 = Label(root, text="Answer the question for candy!", font=("Helvetica", 28), bg="black", fg="red")
        self.label_2.grid(columnspan=6, pady=5, padx=(100, 10))

    # I had to add this label, otherwise it would crash when I try to delete label_7 in selectQuiz() on my first run
    def prime(self):
        self.label_7 = Label(root, text="I serve candy.", font=("Helvetica", 32), bg="black", fg="green")
        self.label_7.grid(columnspan=6, pady=5, padx=(100, 10))

    # Prints select difficulty buttons
    def difficulty(self):
        self.label_8 = Label(root, text="Please choose a difficulty.", font=("Helvetica", 32), bg="black", fg="green")
        self.label_8.grid(columnspan=6, pady=5, padx=(100, 10))

        self.button_8 = Button(root, text="Easy", font=("Helvetica", 36), command=lambda: self.selectQuiz(0))  # lambda allows you to pass an argument
        self.button_8.grid(row=5, column=1, padx=(100, 10))
        self.button_9 = Button(root, text="Medium", font=("Helvetica", 36), command=lambda: self.selectQuiz(1))
        self.button_9.grid(row=5, column=3, padx=(100, 10))
        self.button_10 = Button(root, text="Hard", font=("Helvetica", 36), command=lambda: self.selectQuiz(2))
        self.button_10.grid(row=5, column=5, padx=(100, 10))

        self.label_11 = Label(root, text="Prizes: Easy = 1 candy, Medium = 2 candies, Hard = 3 candies", font=("Helvetica", 16), bg="black", fg="green")
        self.label_11.grid(columnspan=6, pady=5, padx=(100, 10))

    # Randomly selects a question in the correct difficulty
    def selectQuiz(self, difficulty):

        self.label_7.destroy()  # destroys the label from correct() wrong()
        self.label_8.destroy()  # destroys all the labels and buttons from difficulty()
        self.button_8.destroy()
        self.button_9.destroy()
        self.button_10.destroy()
        self.label_11.destroy()

        quantity = (int(len(quiz[difficulty])) - 1)  # gets the number of questions in selected difficulty, cast int to avoid errors
        randomSelection = int(randint(0, quantity))  # randomly selects a number in a valid range
        print(randomSelection)  # prints the number selected to the console. I used this for error checking, but it isnt necessary for the game.

        # pass values to be printed to screen. [difficulty][selection][data]
        self.quizMe(quiz[difficulty][randomSelection][0],  # question
                    quiz[difficulty][randomSelection][1],  # choice1
                    quiz[difficulty][randomSelection][2],  # choice2
                    quiz[difficulty][randomSelection][3],  # choice3
                    quiz[difficulty][randomSelection][4],  # choice4
                    quiz[difficulty][randomSelection][5],  # answerNum
                    difficulty)  # difficulty

    # This method accepts all quiz info and prints it to the screen
    def quizMe(self, question, choice1, choice2, choice3, choice4, correctChoice, difficulty):

        result = [self.wrong, self.wrong, self.wrong, self.wrong,
                  self.wrong]  # array to hold method names for button commands. Prime array by filling with wrong
        result[correctChoice] = self.correct  # assigns correct answer in correct possition

        choice = [choice1, choice2, choice3, choice4]  # array for font sizing
        # check to see what font size is necessary for buttons
        fontSizeB = 36
        for x in range(0, 4):  # cycles through all the choices to find the longest string.
            if len(choice[x]) > 8:
                fontSizeB = 24
        # check to see what font size is necessary for the question. I'm looking for a more dynamic solution.
        fontSizeL = 32
        if len(question) > 30:
            fontSizeL = 30
            if len(question) > 35:
                fontSizeL = 28
                if len(question) > 45:
                    fontSizeL = 22

        # question
        self.label_3 = Label(root, text=question, font=("Helvetica", fontSizeL), bg="black", fg="green")
        self.label_3.grid(columnspan=6, pady=5, padx=(100, 10))

        # choice1
        self.button_1 = Button(root, text=choice1, font=("Helvetica", fontSizeB),
                               command=lambda: result[1](difficulty))  # lambda allows you to pass an argument
        self.button_1.grid(row=4, column=1, pady=5, padx=(100, 10))

        # choice2
        self.button_2 = Button(root, text=choice2, font=("Helvetica", fontSizeB),
                               command=lambda: result[2](difficulty))
        self.button_2.grid(row=4, column=3, sticky=W, padx=(100, 10))

        # choice3
        self.button_3 = Button(root, text=choice3, font=("Helvetica", fontSizeB),
                               command=lambda: result[3](difficulty))
        self.button_3.grid(row=5, column=1, pady=5, padx=(100, 10))

        # choice4
        self.button_4 = Button(root, text=choice4, font=("Helvetica", fontSizeB),
                               command=lambda: result[4](difficulty))
        self.button_4.grid(row=5, column=3, sticky=W, padx=(100, 10))

    # Executes all necessary functions for a correct answer
    def correct(self, difficulty):
        self.clearPage()  # Destroys all buttons and lables on screen before displaying results

        self.label_7 = Label(root, text="CORRECT!!!!", font=("Helvetica", 32), bg="black", fg="green")
        self.label_7.grid(columnspan=6, pady=5, padx=(100, 10))

        self.playSound(correct_audio_path)  # Send the filepath of the audio to play for correct answer
        self.pushCandy((difficulty + 1))  # dispenses appropriate number of candies for difficulty
        self.difficulty()  # asks for difficulty of next question

    # Executes all necessary functions for a wrong answer
    def wrong(self, difficulty):
        self.clearPage()  # Destroys all buttons and lables on screen before displaying results

        self.label_7 = Label(root, text="Wrong, but thanks for playing.", font=("Helvetica", 32), bg="black",
                             fg="green")
        self.label_7.grid(columnspan=6, pady=5, padx=(100, 10))

        self.playSound(incorrect_audio_path)  # Send the filepath of the audio to play for correct answer
        self.pushCandy(1)  # dispenses 1 candy for incorrect guess
        self.difficulty()  # asks for difficulty of next question

    # Pushes the servo in and out to dispense candy, dispenses as much candy as parameter specifies
    def pushCandy(self, candies):

        GPIO.setmode(GPIO.BOARD)  # refers to the pins by the physical position they appear in
        GPIO.setup(7, GPIO.OUT)  # servo on pin 7
        p = GPIO.PWM(7, 50)  # pin 7 pulse width mod, 50hz
        p.start(2.5)  # duty cycle, nutral position

        while candies > 0:
            p.ChangeDutyCycle(
                12)  # Pull plunger. This number may need to be altered depending on your servo and orientation.
            time.sleep(.4)  # Gives the servo time to transition
            p.ChangeDutyCycle(2.5)  # Push plunger. This number may also need to be altered.
            time.sleep(.4)
            candies = candies - 1  # Decrements the count of candies that still need to be dispensed.

        p.stop()  # stops servo control
        GPIO.cleanup()  # cleans the GPIO settings. Without this the servo acts irratically between uses.
        print("candy")  # When testing on desktop, comment all other lines in this method and leave the print to avoid error.

    # play sound from whatever file is at parameter dirrectory. I used this to play a sound effect at multiple points.
    def playSound(self, fileName):
        pygame.mixer.init()
        pygame.mixer.music.load(fileName)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(1)  # change this value if you want to audio to loop.

    # Kills buttons and labels from page after answer is selected
    def clearPage(self):
        self.button_1.destroy()
        self.button_2.destroy()
        self.button_3.destroy()
        self.button_4.destroy()
        self.label_3.destroy()


root = Tk()
root.title("Trick or Trivia")  # adds a name to the titlebar of the application
root.overrideredirect(True)  # This takes up the whole screen and removes x to exit
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),
                                   root.winfo_screenheight()))  # when I was testing on desktop I replaced {0}x{1}+0+0 with the resolution of my touchscreen
root.focus_set()  # <-- move focus to this widget
if (PLATFORM == "FPI"):
    root.configure(background='black', cursor="none")  # removes cursor for a cleaner look, relies on touchscreen. Remove cursor="none" if you need a mouse.
else:
    root.configure(background='black')
app = App(master=root)  # object instantiation
app.header()
app.prime()
app.difficulty()
Button(app, text="X", command=root.destroy, bg="red").pack()
Button(app, text="Theme", bg="white").pack()

app.mainloop()  # This is necessary for event programming in tkinter
