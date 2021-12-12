import socket
from beeper import *
from time import *
from threading import *
from car_controller import MOTOR_DIRECTION_COMMANDS

UPDATE = "UPDATE"

HOST = "192.168.1.147" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

# Need a reference to the car controller so we can send commands to it
car_controller_obj = None

wifi_thread_running = False
wifi_thread: Thread = None

def setup_wifi_thread(_car_controller_obj=None):
    global wifi_thread, wifi_thread_running, car_controller_obj

    car_controller_obj = _car_controller_obj
    wifi_thread_running = True
    wifi_thread = Thread(target=wifi_thread_handler)
    wifi_thread.start()

def wifi_thread_handler():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting with Host {} and Port {}".format(HOST, PORT))
        try:
            s.bind((HOST, PORT))
            s.listen()
        except Exception as e:
            print("Closing Socket With Exception {}".format(e))
        print("Connected Successfully....")
        print("Listening....")
        while 1:
            try:
                client, clientInfo = s.accept()
                data = client.recv(1024)
                data = data.decode("utf-8")
                print("From {}: {}".format(clientInfo[0], data))
                if (data in MOTOR_DIRECTION_COMMANDS):
                    # this is a motor command
                    car_controller_obj.issue_command(data, "-1.0")
                else:
                    # This is a command with two inputs
                    new_data = data.split()
                    car_controller_obj.issue_command(new_data[0], new_data[1])
            except Exception as e:
                print(e)
        client.close()
        s.close()

def wifi_thread_cleanup():
    global wifi_thread_running
    
    wifi_thread_running = False

if __name__ == "__main__":
    setup_wifi_thread()
