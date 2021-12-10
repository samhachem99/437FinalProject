import socket

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
    setup(CLIENT_HOST, CLIENT_PORT)
    
    while True:
        user_text = input("what to send?\n")
        if user_text == "qq":
            send_request(STOP)
            break
        process_request(user_text)
    client.close()
    

