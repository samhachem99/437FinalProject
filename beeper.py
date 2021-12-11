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
    global buzzer_running, interval, running
    
    while buzzer_running:
        if running:
            beep(interval)
    destroy()
        
def destroy():
    global beep_thread, interval, buzzer_running, running
    
    off()
    GPIO.cleanup()
    buzzer_running = False
    beep_thread.join()
    running = 0
    interval = WARNING_ONE_INTERVAL
    

def beep_thread_handler():
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
    
def beep_setup(pin=BUZZER_PIN_DEFAULT, intvl=WARNING_ONE_INTERVAL):
    global beep_thread, interval, running
    
    setup(pin)
    interval = intvl
    running = 0
    beep_thread = Thread(target=beep_thread_handler)
    beep_thread.start()

def beep_control(intvl, active=1):
    global interval, running
    
    if active == 0:
        running = 0
    else: 
        running = 1
        interval = intvl

if __name__ == "__main__":
    beep_setup()
    while True:
        user_text = input("off?\n")
        if user_text.lower() == "1":
            beep_control(WARNING_ONE_INTERVAL)
        elif user_text.lower() == "2":
            beep_control(WARNING_TWO_INTERVAL)
        elif user_text.lower() == "3":
            beep_control(WARNING_THREE_INTERVAL)
        elif user_text.lower() == "u":
            beep_control(WARNING_ONE_INTERVAL, active=0)
        else:
            destroy()
            break
    