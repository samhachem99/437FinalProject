import picar_stuff.picar_4wd as fc
import RPi.GPIO as GPIO
from threading import *
import time

BEEP_INTERVAL_LONG = 0.5
BEEP_INTERVAL_MEDIUM = 0.25
BEEP_INTERVAL_SHORT = 0.13
BEEP_INTERVAL_CONTINUOUS = 0.0

BUZZER_PIN_DEFAULT = "D0"

beep_thread: Thread = None

class Beeper():
    def __init__(self, pin_val=BUZZER_PIN_DEFAULT, interval=BEEP_INTERVAL_LONG):
        self.is_beeping = False
        self.pin = fc.Pin(pin_val)
        self.interval = interval
        self.beep_thread = Thread(target=self.beep_thread_handler)
        self.beep_thread_active = True
        self.beep_thread.start()
    
    def play_beep_sound(self):
        self.pin.value(GPIO.HIGH)
    
    def stop_beep_sound(self):
        self.pin.value(GPIO.LOW)
    
    def play_beep_sequence(self):
        self.play_beep_sound()
        if self.interval != BEEP_INTERVAL_CONTINUOUS:
            time.sleep(self.interval)
            self.stop_beep_sound()
            time.sleep(self.interval)
    
    def set_beep_state(self, intvl, active=1):
        self.is_beeping = active
        self.interval = intvl

    def disable_beeper(self):
        self.stop_beep_sound()
        GPIO.cleanup()
        self.beep_thread_active = False
        self.is_beeping = False
        self.beep_thread.join()
        self.pin = None
        self.interval = BEEP_INTERVAL_CONTINUOUS
        
    def beep_thread_handler(self):
        try:
            while self.beep_thread_active:
                if self.is_beeping:
                    self.play_beep_sequence()
                else:
                    self.stop_beep_sound()
            self.disable_beeper()
        except KeyboardInterrupt:
            self.disable_beeper()

if __name__ == "__main__":
    beeper_obj = Beeper()
    while True:
        user_text = input("off?\n")
        if user_text.lower() == "1":
            beeper_obj.set_beep_state(BEEP_INTERVAL_LONG)
        elif user_text.lower() == "2":
            beeper_obj.set_beep_state(BEEP_INTERVAL_MEDIUM)
        elif user_text.lower() == "3":
            beeper_obj.set_beep_state(BEEP_INTERVAL_SHORT)
        elif user_text.lower() == "4":
            beeper_obj.set_beep_state(BEEP_INTERVAL_CONTINUOUS)
        elif user_text.lower() == "u":
            beeper_obj.set_beep_state(BEEP_INTERVAL_LONG, active=0)
        else:
            beeper_obj.disable_beeper()
            break
    