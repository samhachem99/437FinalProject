import RPi.GPIO as GPIO
import time

buzzer = 26  

def setup(pin):
    global buzzerPin 
    
    buzzerPin = pin 
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(buzzerPin, GPIO.OUT)
    GPIO.output(buzzerPin, GPIO.HIGH)
    
def on():
    GPIO.output(buzzerPin, GPIO.LOW) 
    
def off():
    GPIO.output(buzzerPin, GPIO.HIGH)
    
def beep(x):
    on()
    time.sleep(x)
    off()
    time.sleep(x)
    
def loop(x):
    while True:
        beep(x)
        
def destroy():
    off()
    GPIO.cleanup()
    
if __name__ == "__main__":
    setup(buzzer)
    try:
        loop(0.5)
    except KeyboardInterrupt:
        destroy()