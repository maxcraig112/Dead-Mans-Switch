from pymata4 import pymata4
import time

class Buzzer:
    """
    this class is meant to allow the control of an active buzzer. the current parameters are required
    - board representing an arduino the buzzer is connected to
    - power pin representing the pin it draws power from
    """
    def __init__(self, board, powerPin = 2) -> None:
        #the board that the buzzer is connected to
        self.board = board
        #the power pin that is set to high when the buzzer is being used
        self.powerPin = powerPin

        #initialise pins
        self.initialise_pin()

    def initialise_pin(self):
        """
        Set power pin to digital output, which allows it to be toggled to play a sound
        """
        #set pin to digital output and tie to ground so it begins not playing nothing
        self.board.set_pin_mode_digital_output(self.powerPin)
        self.board.digital_pin_write(self.powerPin,0)
        
    def reset(self):
        """
        Unique reset sound that is played when the 555 timer reset signal is sent and the arduino is about to reset

        INPUT:
        - self representing an instance of the class

        OUTPUT:
        - a unique reset sound
        """
        #Tone and Time are constants that are representing the time between beeps
        #Tone is only used for a pwm signal, otherwise it is set to 1 to represent a HIGH digital output
        TONE = 1
        TIME = 0.5
        #turn buzzer on
        self.board.digital_pin_write(self.powerPin,TONE)
        #wait for a certain amount of time
        time.sleep(TIME)
        #turn buzzer off
        self.board.digital_pin_write(self.powerPin,0)
        #wait for a certain amount of time
        time.sleep(TIME)
        #turn buzzer on
        self.board.digital_pin_write(self.powerPin,TONE)
        #wait for a certain amount of time
        time.sleep(TIME)
        #turn buzzer off
        self.board.digital_pin_write(self.powerPin,0)
    def ramp_up(self):
        """
        unique sound for ramping up of fans
        - tone represents the PWM write to the power pin, if a digital output pin is used set to 1
        - time represents the interval between each tone
        """
        TONE = 1
        TIME = 0.05
        #turn buzzer on
        self.board.digital_pin_write(self.powerPin,TONE)
        #wait for a certain amount of time
        time.sleep(TIME)
        #turn buzzer off
        self.board.digital_pin_write(self.powerPin,0)
        #wait for a certain amount of time
        time.sleep(TIME)
        #turn buzzer on
        self.board.digital_pin_write(self.powerPin,TONE)
        #wait for a certain amount of time
        time.sleep(TIME)
        #turn buzzer off
        self.board.digital_pin_write(self.powerPin,0)

    def ramp_down(self):
        """
        unique sound for ramping down of fans
        - tone represents the PWM write to the power pin, if a digital output pin is used set to 1
        - time represents the interval between each tone
        """
        TONE = 1
        TIME = 0.04
        #turn buzzer on
        self.board.digital_pin_write(self.powerPin,TONE)
        #wait for a certain amount of time
        time.sleep(TIME)
        #turn buzzer off
        self.board.digital_pin_write(self.powerPin,0)
        #wait for a certain amount of time
        time.sleep(TIME)
        #turn buzzer on
        self.board.digital_pin_write(self.powerPin,TONE)
        #wait for a certain amount of time
        time.sleep(TIME)
        #turn buzzer off
        self.board.digital_pin_write(self.powerPin,0)
        #wait for a certain amount of time
        time.sleep(TIME)
        #turn buzzer on
        self.board.digital_pin_write(self.powerPin,TONE)
        #wait for a certain amount of time
        time.sleep(TIME)
        #turn buzzer off
        self.board.digital_pin_write(self.powerPin,0)

if __name__ == "__main__":
    """
    Tester code just to tune ramp up and ramp down
    """
    board = pymata4.Pymata4()
    buzzer = Buzzer(board, 3)
    buzzer.ramp_up()
    time.sleep(1)
    buzzer.ramp_down()