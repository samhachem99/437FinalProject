import socket 

CLIENT_HOST = "192.168.1.147" 
CLIENT_PORT = 8000
BUFFER_SIZE = 4096

client = None

def setup(host, port):
    global client
    
    print("Connecting to Host {} and Port {}".format(host, port))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host,port))
    print("connected....")
    
def process_message(message: str):
    global client 
    
    client.send(message.encode())
    data = str(client.recieve(BUFFER_SIZE).decode("utf-8"))
    print("Client sent back this: {}".format(data))

if __name__ == "__main__":
    host = input("Host IP Address: ")
    port = int(input("Host Port: "))
    setup(host, port)
    
    while True:
        user_text = input("what to send?\n")
        if user_text == "q":
            break
        process_message(user_text)
    

