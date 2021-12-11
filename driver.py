import os
import sys
import time
import picar_4wd as fc

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
fd = None

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
        fc.stop()
    elif cmd == POWER:
        power_val = duration*10

def get_file_data():
    global fd
    
    if os.path.getsize(filename=FILE_NAME) == 0:
        return None
    data = fd.read()
    fd.truncate(0)
    return data
       
def run_driver():
    global fd
    
    print("Listening for file: {}".format(FILE_NAME))
    while True:
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
    run_driver()