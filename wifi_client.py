import socket
import serial
import time

FROWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
STOP = "STOP"
SPEEDUP = "SPEEDUP"
SPEEDDOWN = "SPEEDDOWN"

CLIENT_HOST = "192.168.1.147" 
CLIENT_PORT = 65432
BUFFER_SIZE = 4096

client = None

def setup(host, port):
    global client
    
    print("Connecting to Host {} and Port {}".format(host, port))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host,port))
    print("connected....")
    
def send_request(message: str):
    global client 
    
    client.send(message.encode())
    print("Message Sent.....")
    # data = str(client.recv(BUFFER_SIZE).decode("utf-8"))
    # print("Client sent back this: {}".format(data))
    
def process_request(message: str):
    if message == "w":
        send_request(FROWARD)
    elif message == "a":
        send_request(LEFT)
    elif message == "d":
        send_request(RIGHT)
    elif message == "s":
        send_request(BACKWARD)
    elif message == "=":
        send_request(SPEEDUP)
    elif message == "-":
        send_request(SPEEDDOWN)
    else:
        send_request(STOP)

if __name__ == "__main__":
    # setup(CLIENT_HOST, CLIENT_PORT)
    
    arduino = serial.Serial(port='/dev/tty.usbmodem142301', baudrate=115200, timeout=.1)
    
    try: 
        while True:
            value = arduino.readline()
            print(value)
            try: 
                [x, y] = value.decode("utf-8").split(',')
                print(x, y)
                process_request()
            except: 
                print("not a point")
            time.sleep(1)
    except:
        client.close()
