from pymata4 import pymata4
from eight_segment import Segment_Display
import time

class BitShift:
    """
    This is a class for a bitshift register, which allows other classes to write data to specific indexes, and then when neccessary,
    shift that array out to the bitshift register.

    This bitshift register works with any amount of SN54HC595's connected in series, the quantity just needs to be specified in the
    instantiation.

    In the case of a bitshift register being used in place of a direct write to digital pins on the ArduinoUno, when instantiating other
    component objects, the board variable should be assigned with a BitShift object instead of an ArduinoUno object.

    This means that methods inside this class have the same name as that of the pymata4 class such that the implementation is easier.
    """
    def __init__(self, board, latchPin, dataPin, clockPin, shiftRegisterCount = 1) -> None:
        #the board that the bitshift is connected to
        self.board = board

        #the latch pin to output the registers
        self.latchPin = latchPin

        #a boolean representing if the registers are currently being outputted
        self.latched = True

        #data pin representing individual bits being stored in the register
        self.dataPin = dataPin

        #clock pin that is pulsed when a new bit is sent
        self.clockPin = clockPin

        #represents how many shift registers are being used
        self.shiftRegisterCount = shiftRegisterCount

        #8 bits of data to be written and outputted parallel
        self.data = [0 for _ in range(8 * shiftRegisterCount)]

        #initialise all pins
        self.initialise_pins()
    
    def digital_pin_write(self, index, bit):
        """
        Method is meant to mimic the ArduinoUno, allowing other classes to write to the bitshift array which is then outputted it's pins

        INPUT:
        - self representing an instance of the class
        - index representing the position on the bitshift register that we are writing to
        - bit representing the data being stored, 1 representing a HIGH 5v signal, and 0 representing LOW ground

        OUTPUT:
        - if the index is within the range of the bit shift register, the bit is stored in the appropriate index
        """
        #the index being written to must be within range
        assert 0 <= index < 8 * self.shiftRegisterCount - 1, "index being written to must be valid on bitshift"

        #data should only be written to bitShift if it is not currently being outputted, therefore if the latch pin is not active, latch it
        if not self.latched:
            self.latched = True
            self.board.digital_pin_write(self.latchPin,0)

        #write data to index of list
        self.data[index] = int(bit)
        
    def initialise_pins(self):
        """
        Set the latch, data and clock pins as digital outputs and tie them to ground to begin

        INPUT:
        - self representing an instance of the class
        
        OUTPUT:
        - all of the specified pins are set as digital outputs and tied to ground
        """
        #set all pins to digital outputs
        self.board.set_pin_mode_digital_output(self.latchPin)
        self.board.set_pin_mode_digital_output(self.dataPin)
        self.board.set_pin_mode_digital_output(self.clockPin)

        #tie to ground
        self.board.digital_pin_write(self.latchPin,0)
        self.board.digital_pin_write(self.dataPin,0)
        self.board.digital_pin_write(self.clockPin,0)

    def shift_out(self):
        """
        For every bit in the bitshift array, shift it into the bitshift register and then set the latch pin to high to output it to the pins

        Data is stored into the bitshift register by going through every element in the array in reverse order. for each bit, write it to the
        data pin, and then pulse the clock pin, which shifts that bit into the bitshift register.

        This is repeated for every single bit of data, when that is done, the latchpin is set to high which outputs all the bits to the pins

        INPUT:
        - self representing an instance of the class
        
        OUTPUT:
        - all of the appropriate data is outputted via the bit shift register output pins
        """
        #tie the latchpin to ground so it doesn't output
        self.board.digital_pin_write(self.latchPin,0)

        #for every bit in the shift register array, in reverse order
        for digit in range(8 * self.shiftRegisterCount - 1,-1,-1):
            #write bit to data pin
            self.board.digital_pin_write(self.dataPin,int(self.data[digit]))
            #pulse clock high then low to signify next bit is going to be sent
            self.board.digital_pin_write(self.clockPin,1)
            self.board.digital_pin_write(self.clockPin,0)
        #set latch boolean to false to signify that bitshift is outputting
        self.latched = False
        #tie latch pin to high to output all data in bitshift register
        self.board.digital_pin_write(self.latchPin,1)

if __name__ == "__main__":
    board = pymata4.Pymata4()
    bitshift = BitShift(board,4,7,8,2)
    bitshift.data = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    bitshift.shift_out()
    # bitshift = BitShift(board,5,6,7,1)
    # while True:
    #     for i in range(256):
    #         binn = bin(i)[2:]
    #         binn = ["0" for _ in range(8 - len(binn))] + list(binn)
    #         bitshift.data = binn
    #         bitshift.shift_out()
    #         time.sleep(0.2)
