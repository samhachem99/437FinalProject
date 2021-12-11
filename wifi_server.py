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
power_val = 50
distance_covered = 0.0
speed_cumlative = 0.0
speed_num = 0
avg_speed = 0.0
running = 1
ultra_reading = 100
speedometer: Thread = None
ultra: Thread = None

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
    global ultra_reading
    
    while running:
        ultra_status = fc.get_distance_at(0)
        print("Ultrasonic Sensor reading: {}".format(ultra_status))
        if 35 <= ultra_status <= 50:
            buzzer.beep_control(WARNING_ONE_INTERVAL)
        elif 10 <= ultra_status <= 35:
            buzzer.beep_control(WARNING_TWO_INTERVAL)
        elif 0 <= ultra_status <= 10: 
            buzzer.beep_control(WARNING_THREE_INTERVAL)
        elif ultra_status > 50 or ultra_status == -2:
            print("buzzer sleeping")
            buzzer.beep_control(WARNING_ONE_INTERVAL, active=0)

def fire_up_thread():
    global speedometer, ultra

    fc.start_speed_thread()
    speedometer = Thread(target=speedometer_handler)
    ultra = Thread(target=ultra_handler)
    
    speedometer.start()
    ultra.start()

def process_data(data=""):
    global power_val

    if data != "":
        if data == FROWARD:
            fc.forward(power=power_val)
        elif data == BACKWARD:
            fc.backward(power=power_val)
        elif data == RIGHT:
            fc.turn_right(power=power_val)
        elif data == LEFT:
            fc.turn_left(power=power_val)
        elif data == SPEEDUP:
            power_val = min(100, power_val+10)
        elif data == SPEEDDOWN:
            power_val = max(10, power_val-10)
        elif data == STOP:
            fc.stop()

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

def stop_thread():
    global running 
    
    fc.left_rear_speed.deinit()
    fc.right_rear_speed.deinit()
    speedometer.join()
    ultra.join()
    
    buzzer.destroy()
    running = 0

if __name__ == "__main__":
    buzzer.beep_setup()
    fire_up_thread()
    run_server()
    stop_thread()
