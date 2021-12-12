from time import *
from threading import *
from beeper import *
import picar_stuff.picar_4wd as fc

# commands acceptable
FORWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
STOP = "STOP"
MOTOR_COMMANDS = [FORWARD, BACKWARD, LEFT, RIGHT, STOP]
POWER = "POWER"

# For the motor thread
power_val = 50
motor_command_queue = []
motor_move_state = STOP
motor_active_duration = -1
WALL_DISTANCE_THRESHOLD = 10

# For the ultrasonic thread
ultrasonic_reading = -1

# For all threads
threads_running = False
ultrasonic_thread: Thread = None
motor_thread: Thread = None
collision_detector_thread: Thread = None

def ultrasonic_handler():
    global threads_running, ultrasonic_reading
    
    i = 0
    while threads_running:
        ultrasonic_reading = fc.get_distance_at(0)
        print("ultra reading: {}".format(ultrasonic_reading))
        if i % 5:
            if 30 <= ultrasonic_reading < 40:
                set_beep_state(BEEP_INTERVAL_LONG)
            elif 20 <= ultrasonic_reading < 30:
                set_beep_state(BEEP_INTERVAL_MEDIUM)
            elif 10 <= ultrasonic_reading < 20: 
                set_beep_state(BEEP_INTERVAL_SHORT)
            elif 0 <= ultrasonic_reading < 10:
                set_beep_state(BEEP_INTERVAL_CONTINUOUS)
            elif ultrasonic_reading >= 40 or ultrasonic_reading < 0:
                set_beep_state(BEEP_INTERVAL_LONG, active=0)
        i += 1
        sleep(1)

# Moves the car in a certain direction for a determined duration
# after which the car stops
def motor_command(command, duration, _power_val):
    global motor_move_state
    
    motor_move_state = command

    if command == FORWARD:
        fc.forward(power=_power_val)
    elif command == BACKWARD:
        fc.backward(power=_power_val)
    elif command == RIGHT:
        fc.turn_right(power=_power_val)
    elif command == LEFT:
        fc.turn_left(power=_power_val)
    elif command == STOP:
        fc.stop()
    
    if (duration != -1):
        sleep(duration)
    stopCar()

def stopCar():
    global motor_move_state
    
    if (motor_move_state != STOP):
        motor_move_state = STOP
        fc.stop()

def isCarCloseToWall():
    global ultrasonic_reading

    return (0 <= ultrasonic_reading <= WALL_DISTANCE_THRESHOLD)

def motor_handler():
    global motor_command_queue

    while threads_running:
        if (len(motor_command_queue) > 0):
            item = motor_command_queue[0]
            command = item[0]
            duration = item[1]
            power = item[2]
            motor_command(command, duration, power)
            motor_command_queue.pop(0)
    

# The thread responsible for collision detection
def collision_detector_handler():
    while threads_running:
        if (motor_move_state == FORWARD and isCarCloseToWall()):
            stopCar()

def setup_threads():
    global ultrasonic_thread, motor_thread

    fc.start_speed_thread()
    ultrasonic_thread = Thread(target=ultrasonic_handler)
    collision_detector_thread = Thread(target=collision_detector_handler)
    motor_thread = Thread(target=motor_handler)
    
    ultrasonic_thread.start()
    collision_detector_thread.start()
    motor_thread.start()

def stop_treads():
    global threads_running 

    threads_running = False
    beep_thread_cleanup()
    
    fc.left_rear_speed.deinit()
    fc.right_rear_speed.deinit()
    
    ultrasonic_thread.join()
    collision_detector_thread.join()
    motor_thread.join()


def issue_command(command: str, input: str=""):
    global motor_thread, motor_command_queue, power_val, motor_move_state

    if command in MOTOR_COMMANDS:
        try:
            if (motor_thread == None):
                duration = float(input)

                # If the duration is more than 0, the command should be queued.
                # If it is less than 0, the command should interrupt the motor_command_queue
                # and be executed immediately
                if (duration >= 0.0):
                    motor_command_queue.append((command, duration, power_val))
                else:
                    motor_command_queue = []
                    motor_move_state = command
                    motor_command(command, duration, power_val)
        except Exception as e:
            print(e)
    elif command == POWER:
        try:
            power_val = float(input)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    setup_threads()
    issue_command("LEFT", "1.0")
    issue_command("RIGHT", "1.0")
    issue_command("STOP", "1.0")
    issue_command("LEFT", "1.0")
