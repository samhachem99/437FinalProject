import socket
# import serial
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
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((CLIENT_HOST,CLIENT_PORT))
    
def send_request(message: str):
    global client 
    print("in sending mesage: {}".format(message))
    
    client.send(message.encode())
    ataFromServer = client.recv(0);
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
    
    # arduino = serial.Serial(port='/dev/tty.usbmodem142301', baudrate=115200, timeout=.1)
    print("Connecting to Host {} and Port {}".format(CLIENT_HOST, CLIENT_PORT))
    try: 
        while True:
            setup(CLIENT_HOST, CLIENT_PORT)
            print("Connected...")
            usr_val = input("what is your command?\n")
            if usr_val == "qq":
                break
            process_request(usr_val)
            # value = arduino.readline()
            # print(value)
            # try: 
            #     [x, y] = value.decode("utf-8").split(',')
            #     print(x, y)
            #     process_request()
            # except: 
            #     print("not a point")
            # time.sleep(1)
            client.close()
    except Exception as e:
        print(e)
        client.close()
    client.close()
