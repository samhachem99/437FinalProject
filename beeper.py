import picar_4wd as fc
import RPi.GPIO as GPIO
from threading import *
import time

WARNING_ONE_INTERVAL = 0.5 
WARNING_TWO_INTERVAL = 0.25
WARNING_THREE_INTERVAL = 0.13

BUZZER_PIN_DEFAULT = "D0"

running = 0
pin: fc.Pin = None
buzzer_running = True
interval = WARNING_ONE_INTERVAL

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

def beep_launch(intvl=WARNING_ONE_INTERVAL):
    global beep_thread, interval, running
    
    interval = intvl
    running = 1
    beep_thread = Thread(target=beep_thread_handler)
    beep_thread.start()
    
def beep_turn_off():
    global beep_thread, interval, buzzer_running, running
    
    buzzer_running = False
    beep_thread.join()
    running = 0
    interval = WARNING_ONE_INTERVAL
    
def beep_setup(pin=BUZZER_PIN_DEFAULT):
    setup(pin)

if __name__ == "__main__":
    beep_setup()
    beep_launch()
    while True:
        user_text = input("off?\n")
        if user_text.lower() == "1":
            interval = WARNING_ONE_INTERVAL
        elif user_text.lower() == "2":
            interval = WARNING_TWO_INTERVAL
        elif user_text.lower() == "3":
            interval = WARNING_THREE_INTERVAL
        else:
            beep_turn_off()
            break
    