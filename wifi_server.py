import socket
from beeper_test import WARNING_ONE_INTERVAL, WARNING_THREE_INTERVAL, WARNING_TWO_INTERVAL
import picar_4wd as fc
import json
from time import *
from threading import *
import beeper as buzzer

FROWARD = "FORWARD"
BACKWARD = "BACKWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
STOP = "STOP"
SPEEDUP = "SPEEDUP"
SPEEDDOWN = "SPEEDDOWN"
UPDATE = "UPDATE"
HOST = "192.168.1.147" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
current_command = STOP
power_val = 50
distance_covered = 0.0
speed_cumlative = 0.0
speed_num = 0
avg_speed = 0.0
running = 1
ultra_reading = 100

speedometer: Thread = None
ultra: Thread = None
motor_thread: Thread = None

def speedometer_handler():
    global speed_num
    global speed_cumlative
    global avg_speed
    global distance_covered
    global running

    while running:
        first_speed = fc.speed_val()
        sleep(1)
        current_speed = fc.speed_val()
        distance_covered += ((first_speed + current_speed)/2) * 1

def ultra_handler():
    global running, ultra_reading
    
    while running:
        ultra_status = fc.get_distance_at(0)
        print("ultra reading: {}".format(ultra_status))
        if 30 <= ultra_status < 40:
            buzzer.beep_control(WARNING_ONE_INTERVAL)
        elif 20 <= ultra_status < 30:
            buzzer.beep_control(WARNING_TWO_INTERVAL)
        elif 10 <= ultra_status < 20: 
            buzzer.beep_control(WARNING_THREE_INTERVAL)
        elif 0 <= ultra_status < 10:
            buzzer.beep_control(buzzer.WARNING_FOUR_INTERVAL)
        elif ultra_status >= 40 or ultra_status < 0:
            buzzer.beep_control(WARNING_ONE_INTERVAL, active=0)
        sleep(1)
        
def motor_thread_handler():
    global running, current_command
    
    while running:
        ultra_status = fc.get_distance_at(0)
        if current_command == FROWARD:
            if ultra_status <= 5:
                fc.stop()
            else:
                motor_command()
        elif current_command == RIGHT or current_command == LEFT:
            if ultra_status <= 5:
                fc.backward()
                sleep(0.5)
            motor_command()
        else:
            motor_command()

def fire_up_thread():
    global speedometer, ultra, motor_thread

    fc.start_speed_thread()
    speedometer = Thread(target=speedometer_handler)
    ultra = Thread(target=ultra_handler)
    motor_thread = Thread(target=motor_thread_handler)
    
    speedometer.start()
    ultra.start()
    motor_thread.start()
    
def motor_command():
    global power_val, current_command
    
    if current_command == FROWARD:
        fc.forward(power=power_val)
    elif current_command == BACKWARD:
        fc.backward(power=power_val)
    elif current_command == RIGHT:
        fc.turn_right(power=power_val)
    elif current_command == LEFT:
        fc.turn_left(power=power_val)
    elif current_command == STOP:
            fc.stop()

def process_data(data=""):
    global power_val, current_command

    if data != "":
        if data == SPEEDUP:
            power_val = min(100, power_val+10)
        elif data == SPEEDDOWN:
            power_val = max(10, power_val-10)
        else:
            current_command = data

def send_feedback(data):
    global power_val
    
    direction = ""
    if data not in [STOP, SPEEDUP, SPEEDDOWN, UPDATE]:
        direction = data.lower()
    power = str(round(fc.power_read(), 2)) + "V"
    speed_val = str(round(fc.speed_val(), 2)) + "cm/s"
    distance = str(round(distance_covered, 2)) + "cm"
    temp = str(round(fc.cpu_temperature(), 2)) + "C"
    ultra_val = str(round(fc.get_distance_at(0))) + "cm"
    ret_data = {
        'direction': direction,
        'power': power,
        'speed': speed_val,
        'distance': distance,
        'temp': temp,
        'ultra': ultra_val,
        'power_val': power_val
    }
    return json.dumps(ret_data)

def run_server():
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
                process_data(data)
                client.sendall(bytes(send_feedback(data), "utf-8"))
            except Exception as e:
                print(e)
        client.close()
        s.close()
        buzzer.destroy()

def stop_thread():
    global running 
    buzzer.destroy()
    
    fc.left_rear_speed.deinit()
    fc.right_rear_speed.deinit()
    speedometer.join()
    ultra.join()
    
    running = 0

if __name__ == "__main__":
    buzzer.beep_setup()
    fire_up_thread()
    run_server()
    stop_thread()
