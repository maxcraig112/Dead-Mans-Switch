from pymata4 import pymata4
from bitShift import BitShift
from anode_eight_segment import Segment_Display
from buzzer import Buzzer
from button import Button
from counter import Counter
import time


ENABLE_OUTPUT = 4
DATA_PIN = 7
CLOCK_PIN = 2
BUZZER = 3

DEADMANS_SWITCH_DURATION = 99

def count_one_second(seg,counter):
    time_start = time.time()
    while time.time() - time_start <= 1:
        seg.print_word(str(counter.count))
        time.sleep(0.01)
        seg.reset_display()
        time.sleep(0.01)

if __name__ == "__main__":
    #initialise the arduinoUno class
    board = pymata4.Pymata4()
    #intialise the bitshift registers
    bitshift = BitShift(board,ENABLE_OUTPUT,DATA_PIN,CLOCK_PIN,2)

    #initialise the segment display
    seg = Segment_Display(bitshift,[0,3,4,11],[1,5,9,7,6,2,10,8])

    counter = Counter(DEADMANS_SWITCH_DURATION)

    button = Button(board,counter,14)
    buzzer = Buzzer(board, BUZZER)


    buzzer.ramp_up()

    start = time.time()
    while counter.count != 0:
        count_one_second(seg,counter)
        counter.decrement()

    seg.rolling_sentence("Alarm")
    for i in range(10):
        buzzer.ramp_up()
        time.sleep(1)
        

    

