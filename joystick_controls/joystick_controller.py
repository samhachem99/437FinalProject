import serial
import time

arduino = serial.Serial(port='/dev/tty.usbmodem142301', baudrate=115200, timeout=.1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

def read_serial():
    data = arduino.readline()
    return data

if __name__ == "__main__":
    while True:
        # num = input("Enter a number: ") # Taking input from user
        value = read_serial()
        print(value) # printing the value
        time.sleep(1)
