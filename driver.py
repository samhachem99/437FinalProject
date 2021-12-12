import file_listener
import car_controller

def initialize_driver():
    file_listener.setup_file_listener_thread()
    car_controller.setup_threads()

if __name__ == "__main__":
    initialize_driver()
