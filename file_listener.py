import os
import time
import picar_stuff.picar_4wd as fc
from threading import *

# commands acceptable
FROWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
STOP = "STOP"
POWER = "POWER"
COMMANDS_CONSTS = [FROWARD, BACKWARD, LEFT, RIGHT]
FILE_NAME = "commands.txt"

power_val = 50

# Thread active flags
file_listener_active = False

# Threads
file_listener_thread: Thread = None

def process_data(cmd: str, duration: float):
    global power_val
    
    print("processing: {} for {}".format(cmd, duration))
    if cmd in COMMANDS_CONSTS:
        if cmd == FROWARD:
            fc.forward(power=power_val)
        elif cmd == BACKWARD:
            fc.backward(power=power_val)
        elif cmd == RIGHT:
            fc.turn_right(power=power_val)
        elif cmd == LEFT:
            fc.turn_left(power=power_val)
        time.sleep(duration)
        fc.stop()
    elif cmd == STOP:
        time.sleep(duration)
    elif cmd == POWER:
        power_val = duration*10

def get_file_data(fd):
    if os.path.getsize(filename=FILE_NAME) == 0:
        return None
    data = fd.read()
    fd.truncate(0)
    return data

def setup_file_listener_thread():
    global file_listener_active, file_listener_thread

    file_listener_thread = Thread(target=file_listener_thread_handler)
    file_listener_active = True
    file_listener_thread.start()

def file_listener_thread_cleanup():
    global file_listener_active

    file_listener_active = False
    file_listener_thread.join()

def file_listener_thread_handler():
    print("Listening for file: {}".format(FILE_NAME))
    while file_listener_active:
        fd = open(FILE_NAME, "r+")
        data = get_file_data()
        if data != None:
            commands_list = data.split('\n')
            for command in commands_list:
                try: 
                    cmd_duration = command.strip().split(' ')
                    process_data(cmd_duration[0].upper(), float(cmd_duration[1]))
                except:
                    continue
        fd.close()
        time.sleep(0.5)

if __name__ == "__main__":
    setup_file_listener_thread()
