import file_listener
import wifi_server
import car_controller

def initialize_driver():
    car_controller.setup_threads()
    file_listener.setup_file_listener_thread(car_controller)
    wifi_server.setup_wifi_thread(car_controller)

if __name__ == "__main__":
    initialize_driver()
