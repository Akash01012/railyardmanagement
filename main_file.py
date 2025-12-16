from engine_file import Engine
from wagon_file import Wagon
from guardvan_file import GuardVan
import sys

# Ensure prints flush immediately
sys.stdout.reconfigure(line_buffering=True)

class Device:
    def __init__(self) -> None:
        pass

def create_device(device_id, partner_id, unique_id, device_type, wagons_obj):
    if device_type == "Wagon":
        return Wagon(device_id, partner_id, unique_id)
    elif device_type == "Engine":
        if wagons_obj is None:
            print("Empty Wagons References....")
            return None
        return Engine(device_id, partner_id, unique_id, wagons_obj)
    elif device_type == "GuardVan":
        return GuardVan(device_id, partner_id, unique_id)
    else:
        print("Please choose the correct type...........")
        return None

def setup_devices():
    # Wagons and Guard Vans
    device_3 = create_device("D3","D4","C1","Wagon",None)
    device_4 = create_device("D4","D3","C1","Wagon",None)
    device_5 = create_device("D5","D6","C2","Wagon",None)
    device_6 = create_device("D6","D5","C2","Wagon",None)
    device_7 = create_device("D7","D8","G1","GuardVan",None)
    device_8 = create_device("D8","D7","G1","GuardVan",None)

    # Pair wagons and guard vans
    device_3.adding_partner(device_4)
    device_4.adding_partner(device_3)
    device_5.adding_partner(device_6)
    device_6.adding_partner(device_5)
    device_7.adding_partner(device_8)
    device_8.adding_partner(device_7)

    device_4.assing_next_wagon(device_5)
    device_6.assing_next_wagon(device_7)

    wagons_obj1 = [device_3, device_4, device_5, device_6, device_7]

    # Engines
    device_1 = create_device("D1","D2","E1","Engine",wagons_obj1)
    device_2 = create_device("D2","D1","E1","Engine",wagons_obj1)
    device_1.adding_partner(device_2)
    device_2.adding_partner(device_1)
    device_2.assing_next_wagon(device_3)

    engines_obj = [device_1, device_2]
    return engines_obj

class ControlRoom:
    def __init__(self, engines):
        self.engines = engines
        self.trains = []

    def receive_command_response(self, sender):
        print(f"Received the list from Engine: {sender.originator_id}", flush=True)

    def send_command(self, command):
        print(f"Sending {command} command to everyone", flush=True)
        for engine in self.engines:
            response = engine.process_command(self, command)
            if response is None:
                continue
            self.trains.append(response)

def run_simulation():
    engines_obj = setup_devices()
    control_room = ControlRoom(engines_obj)

    control_room.send_command("attched_wagons_list")

    print("\nAttached wagon list")
    print(".....................................................")
    for train in control_room.trains:
        print(train)

if __name__ == "__main__":
    run_simulation()