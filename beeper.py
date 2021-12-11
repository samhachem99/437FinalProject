import picar_4wd as fc
import RPi.GPIO as GPIO
import time

WARNING_ZERO_INTERVAL = 1
WARNING_ONE_INTERVAL = 0.5 
WARNING_TWO_INTERVAL = 0.25
WARNING_THREE_INTERVAL = 0.13

buzzer_pin = "D0"

pin: fc.Pin = None
buzzer_running = True

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
    
def loop(x):
    global buzzer_running
    
    while buzzer_running:
        beep(x)
        
def destroy():
    off()
    GPIO.cleanup()

def launch():
    setup(buzzer_pin)
    try:
        loop(WARNING_ONE_INTERVAL)
    except KeyboardInterrupt:
        destroy()
        
if __name__ == "__main__":
    launch()
    user_text = input("off?")
    if user_text.lower() == "y":
        buzzer_running = False
        

    