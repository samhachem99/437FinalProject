import picar_4wd as fc
import RPi.GPIO as GPIO
from threading import *
import time

WARNING_ZERO_INTERVAL = 1
WARNING_ONE_INTERVAL = 0.5 
WARNING_TWO_INTERVAL = 0.25
WARNING_THREE_INTERVAL = 0.13

BUZZER_PIN_DEFAULT = "D0"

pin: fc.Pin = None
buzzer_running = True
interval = WARNING_ZERO_INTERVAL

beep_thread: Thread = None

def setup(pin_val):
    global pin
    
    pin = fc.Pin(pin_val)
    
def on():
    global pin
    pin.value(GPIO.LOW)
    
def off():
    global pin
    pin.value(GPIO.HIGH)
    
def beep(x):
    on()
    time.sleep(x)
    off()
    time.sleep(x)
    
def loop():
    global buzzer_running, interval
    
    while buzzer_running:
        beep(interval)
    destroy()
        
def destroy():
    off()
    GPIO.cleanup()

def beep_thread_handler():
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

def launch(intvl=WARNING_ZERO_INTERVAL):
    global beep_thread, interval
    
    interval = intvl
    beep_thread = Thread(target=beep_thread_handler)
    beep_thread.start()

if __name__ == "__main__":
    setup(BUZZER_PIN_DEFAULT)
    launch()
    while True:
        user_text = input("off?\n")
        if user_text.lower() == "0":
            interval = WARNING_ZERO_INTERVAL
        elif user_text.lower() == "1":
            interval = WARNING_ONE_INTERVAL
        elif user_text.lower() == "2":
            interval = WARNING_TWO_INTERVAL
        elif user_text.lower() == "3":
            interval = WARNING_THREE_INTERVAL
        else:
            buzzer_running = False
            break
        

    