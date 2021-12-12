import picar_stuff.picar_4wd as fc
import RPi.GPIO as GPIO
from threading import *
import time

BEEP_INTERVAL_LONG = 0.5
BEEP_INTERVAL_MEDIUM = 0.25
BEEP_INTERVAL_SHORT = 0.13
BEEP_INTERVAL_CONTINUOUS = 0.0

BUZZER_PIN_DEFAULT = "D0"

is_beeping = 0
pin: fc.Pin = None
beep_thread_active = True
interval = BEEP_INTERVAL_LONG

beep_thread: Thread = None

def play_beep_sound():
    global pin
    pin.value(GPIO.HIGH)
    
def stop_beep_sound():
    global pin
    pin.value(GPIO.LOW)
    
def play_beep_sequence_for_duration(duration):
    play_beep_sound()
    if duration != BEEP_INTERVAL_CONTINUOUS:
        time.sleep(duration)
        stop_beep_sound()
        time.sleep(duration)
        
def beep_thread_cleanup():
    global beep_thread, interval, beep_thread_active, is_beeping
    
    stop_beep_sound()
    GPIO.cleanup()
    beep_thread_active = False
    beep_thread.join()
    is_beeping = 0
    interval = BEEP_INTERVAL_LONG

def beep_thread_handler():
    global beep_thread_active, interval, is_beeping

    try:
        while beep_thread_active:
            if is_beeping:
                play_beep_sequence_for_duration(interval)
            else:
                stop_beep_sound()
        beep_thread_cleanup()
    except KeyboardInterrupt:
        beep_thread_cleanup()
    
def beep_setup(pin_val=BUZZER_PIN_DEFAULT, intvl=BEEP_INTERVAL_LONG):
    global beep_thread, interval, is_beeping, pin
    
    pin = fc.Pin(pin_val)
    interval = intvl
    is_beeping = 0
    beep_thread = Thread(target=beep_thread_handler)
    beep_thread.start()

def set_beep_state(intvl, active=1):
    global interval, is_beeping
    
    is_beeping = active
    interval = intvl

if __name__ == "__main__":
    beep_setup()
    while True:
        user_text = input("off?\n")
        if user_text.lower() == "1":
            set_beep_state(BEEP_INTERVAL_LONG)
        elif user_text.lower() == "2":
            set_beep_state(BEEP_INTERVAL_MEDIUM)
        elif user_text.lower() == "3":
            set_beep_state(BEEP_INTERVAL_SHORT)
        elif user_text.lower() == "4":
            set_beep_state(BEEP_INTERVAL_CONTINUOUS)
        elif user_text.lower() == "u":
            set_beep_state(BEEP_INTERVAL_LONG, active=0)
        else:
            beep_thread_cleanup()
            break
    