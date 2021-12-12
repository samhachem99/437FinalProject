import file_listener
import wifi_server
import car_controller

def initialize_driver():
    file_listener.setup_file_listener_thread(car_controller)
    # wifi_server.setup_wifi_thread(car_controller)
    car_controller.setup_threads()

if __name__ == "__main__":
    initialize_driver()
