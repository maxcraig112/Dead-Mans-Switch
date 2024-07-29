
from pymata4 import pymata4
import time

######################################################################
# 12 PIN 8 SEGMENT DISPLAY
######################################################################
class Segment_Display():
    """
    This class is used to instantiate a Segment_Display Object
    This object initialises the given pins, resets the display, and then allows you to write characters, words and sentences to any position on the display
    """
    def __init__(self, board, digit_pins: list = [2,3,4,5], segment_pins: list = [6,7,8,9,10,11,12,13]) -> None:
        
        #assertions to ensure correct parameters are entered

        #the number of digit pins must be 4
        assert len(digit_pins) == 4, "number of declared digit_pins must be 4"
        #the number of segment pins must be 8
        assert len(segment_pins) == 8, "number of segment pins must be 8"

        #board represents an Instantiated ArduinoUno Board, or a Bitshift register
        self.board = board
        
        #declare digit and segment pins for Segment_Display, if no parameter is given it is automatically assigned 2,3,4,5 for digit_pins and 6,7,8,9,10,11,12,13 for segment_pins
        self.digit_pins = {
        "3":digit_pins[0],
        "2":digit_pins[1],
        "1":digit_pins[2],
        "0":digit_pins[3]}

        self.segment_pins = {
        "a": segment_pins[0],
        "b": segment_pins[1],
        "c": segment_pins[2],
        "d": segment_pins[3],
        "e": segment_pins[4],
        "f": segment_pins[5],
        "g": segment_pins[6],
        "dec": segment_pins[7]
        }

        #Initialise all required pins to digital outputs
        self.initialise_pins()
        #reset all values of the display to 0 so nothing is showing
        self.reset_display()

    #charLookup is a dictionary that contains the appropriate data that should be given to the segment pins for each character
    charLookup = {
    " ": "11111111",
    "0": "00000011",
    "1": "10011111",
    "2": "00100101",
    "3": "00001101",
    "4": "10011001",
    "5": "01001001",
    "6": "01000001",
    "7": "00011111",
    "8": "00000001",
    "9": "00001001",
    "a": "00010001",
    "b": "11000001",
    "c": "01100011",
    "d": "10000101",
    "e":"01100001",
    "f":"01110001",
    "g":"01000011",
    "h":"10010001",
    "i":"111100111",
    "j":"100001111",
    "k":"11110001",
    "l":"11100011",
    "m":"00111011",
    "n":"11010101",
    "o":"11000101",
    "p":"00110001",
    "q":"00011001",
    "r":"11110101",
    "s":"01001001",
    "t":"11100001",
    "u":"11000111",
    "v":"10000011",
    "w":"10000001",
    "x":"10010001",
    "y":"10001001",
    "z":"10110101",
    }

    def initialise_pins(self):
        """
        Initialises all of the pins used by the 8-segment display to digital outputs

        INPUT
        - self representing and instance of the class

        OUTPUT
        - a segment display that has all of it's pins set to digital outputs
        - if segment display is connected to a bitshift, this will be ignored
        """
        #for all 12 pins used in 8-segment display, set as digital output
        #all this does is just get the first pin of the digit_pins and the 
        #last pin of the segment_pins and increment through them

        #try to initialise digital pins, if it doesn't let you, it means the segment display is being interfaced through a bitshift register
        try:
            for i in range(list(self.digit_pins.values())[0],list(self.segment_pins.values())[-1] + 1 ):
                #initialise pin as digital output
                self.board.set_pin_mode_digital_output(i)
        except:
            #print to console to let us know that the eight segment is being interfaced through a bitshift
            print("EIGHT SEGMENT INTERFACED THROUGH BITSHIFT")
        

    def reset_display(self, index = None):
        """
        INPUT:
        - self representing an instance of the class
        - an optional index parameter representing which digit you would like to reset
            - if index is None, reset all digits
        
        OUTPUT:
        the display digit pin being tied to high (5v), therefore disabling it

        if Index = None, resets all digits of the display, by writing 1 to their pins. Otherwise, only reset the specific digit specified
        """
        #set all digit pins to 1, essentially turning them off
        #if index is None, reset all digits, otherwise reset specific digit
        if index is None:
            #for every digits pin
            for digit in range(len(self.digit_pins.values())):
                self.board.digital_pin_write(list(self.digit_pins.values())[digit],0)
        else:
            self.board.digital_pin_write(self.digit_pins[str(index)],0)

    def reset_segment(self):
        """
        INPUT: self representing an instance of the class

        OUTPUT: all segment pins of the given segment display being tied to ground
        
        Resets all segment pins, writing them to 0 (tying to ground)
        """
        #for every segment pin
        for i in range(len(self.segment_pins.values())):
            #set segment to 0
            self.board.digital_pin_write(list(self.segment_pins.values())[i],1)

    def print_char(self, char, index):
        """
        INPUT:
        - self representing an instance of the class
        - char representing the character that wants to be displayed
        - index representing which position on the display you want to display the character on

        OUTPUT:
        - the given character being written to the index specified

        print a character (0-9 or a-z) to the specified digit of the display
        """
        #string must be of length 1, or length 2 with one of the characters being a "."
        assert len(char) == 1 or (len(char) == 2 and "." in char), "char must be length 1"

        #convert character to lower case (adds robustness)
        char = char.lower()
        #reset digit (set all segments to 0)
        self.reset_segment()
        #reset display to 1
        self.reset_display(index)

        #set chosen digit to 0 (enabling it)
        self.board.digital_pin_write(self.digit_pins[str(index)],1)
        #for every segment
        for i in range(8):
            #check lookup table, set pin to 1 if needs to be enabled
            self.board.digital_pin_write(list(self.segment_pins.values())[i],int(self.charLookup[str(char)[0]][i]))
        #if there is a decimal in the given character, that tie the decimal segment pin to high
        if "." in char:
            self.board.digital_pin_write(self.segment_pins["dec"],0)
        
    def print_word(self, word):
        """
        INPUT:
        - self representing an instance of the class
        - word representing the word that wants to be displayed
            - the word must be length 4 or less

        prints a word to the display, if the word is less than length 4, nothing is written to the leftover displays
        """
        #the length of the word must be <= 4, not including the decimal points
        assert len(word) - word.count(".") <= 4 , "length of word must be <= 4 (not including decimal points)"

        #declare variables list
        characters = []
        i = 0
        #this section of code basically takes all characters in the word, and joins them to their corresponding decimal point if there is one
        #this is needed so that if there are decimal points, so they can be displayed to the appropriate digit
        while i < len(word):
            if i + 1 < len(word) and word[i+1] == ".":
                characters.append(word[i:i+2])
                i += 1
            else:
                characters.append(word[i])
            i += 1

        #reset segments (set all segments to 1)
        self.reset_segment()

        #reset all displays to 0
        self.reset_display()

        #for all letters in word (decrementing from end of word to start)
        for index in range(-1,-len(characters) - 1,-1):
            #print the character to it's index
            self.print_char(characters[index],-index - 1)
            #try to run the shift out method, it will execute if the eight segment is connected to a bitshift register, otherwise it will not
            try:
                self.board.shift_out()
            except:
                pass
            #reset the entire display (this removes the character, but it runs so quickly it can still be seen)
            self.reset_display(-index-1)

    def rolling_sentence(self, sentence):
        """
        INPUT:
        - self representing an instance of the class
        - sentence representing a sentence that wants to be displayed

        Takes a sentence as input and rolls it across the display. Once the entire sentence has been written, it writes an additional 4 spaces to clear the entire display
        """
        #declare variables list
        characters = []
        i = 0
        #this section of code basically takes all characters in the word, and joins them to their corresponding decimal point if there is one
        #this is needed so that if there are decimal points, it can be displayed to the appropriate digit
        while i < len(sentence):
            if i + 1 < len(sentence) and sentence[i+1] == ".":
                characters.append(sentence[i:i+2])
                i += 1
            else:
                characters.append(sentence[i])
            i += 1
        
        #for every letter of sentence
        for char in range(len(characters) + 5):
            
            #this for loop just increases the amount of time the digit is shown on screen for, so that it moves slower
            for _ in range(7):
                #for every digit of display
                for i in range(4):
                    #This code basically checks if the current digit should be displayed to the screen, and at what position
                    #if no character is meant to be displayed at that particular index, then " " is written, which is all 0's
                    if (char - i) < 0 or (char - i >= len(characters)):
                        self.print_char(" ",i)
                        #try to run the shift out method, it will execute if the eight segment is connected to a bitshift register, otherwise it will not
                        try:
                            self.board.shift_out()
                        except:
                            pass
                        #reset display so next digit can be written
                        self.reset_display(i)
                    else:
                        self.print_char(characters[char - i],i)
                        #try to run the shift out method, it will execute if the eight segment is connected to a bitshift register, otherwise it will not
                        try:
                            self.board.shift_out()
                        except:
                            pass
                        #reset display so next digit can be written
                        self.reset_display(i)


