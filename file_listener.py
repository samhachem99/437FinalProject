import os
import time
import picar_stuff.picar_4wd as fc
from threading import *

# commands acceptable
FILE_NAME = "commands.txt"
car_controller = None

# Thread active flags
file_listener_active = False

# Threads
file_listener_thread: Thread = None

def get_file_data(fd):
    if os.path.getsize(filename=FILE_NAME) == 0:
        return None
    data = fd.read()
    fd.truncate(0)
    return data

def setup_file_listener_thread(_car_controller):
    global file_listener_active, file_listener_thread, car_controller

    car_controller = _car_controller

    file_listener_thread = Thread(target=file_listener_thread_handler)
    file_listener_active = True
    file_listener_thread.start()

def file_listener_thread_cleanup():
    global file_listener_active

    file_listener_active = False
    file_listener_thread.join()

def file_listener_thread_handler():
    global car_controller

    print("Listening for file: {}".format(FILE_NAME))
    while file_listener_active:
        fd = open(FILE_NAME, "r+")
        data = get_file_data(fd)
        if data != None:
            commands_list = data.split('\n')
            for command in commands_list:
                try: 
                    cmd_duration = command.strip().split(' ')
                    car_controller.issue_command(cmd_duration[0].upper(), cmd_duration[1])
                except:
                    continue
        fd.close()
        time.sleep(0.5)

if __name__ == "__main__":
    setup_file_listener_thread()
