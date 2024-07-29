from pymata4 import pymata4
from counter import Counter
import time
class Button:

    def __init__(self,board: pymata4.Pymata4,counter: Counter, pin = 0):
        self.board = board

        self.counter = counter

        self.pin = pin

        self.initialise_pin()
        
        self.lastTimePressed = time.time()

    def button_callback(self,data):
        time.sleep(0.1)
        if data[2] == 1 and abs(time.time() - self.lastTimePressed) > 5:
            self.lastTimePressed = time.time()
            print("resetting")
            self.counter.reset()
            

    def initialise_pin(self):
        """
        Set power pin to digital output, which allows it to be toggled to play a sound
        """
        #set pin to digital output and tie to ground so it begins not playing nothing
        # self.board.set_pin_mode_analog_input(self.analogIn,self.button_callback)
        self.board.set_pin_mode_digital_input(self.pin,self.button_callback)
        print(f"Initialized pin {self.pin} as digital input with callback")
    

