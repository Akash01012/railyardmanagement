import time
class Engine:
    def __init__(self,device_id,partner_id,uid,wagons_obj):
        self.originator_id = uid
        self.wagon_id = uid
        self.device_id = device_id
        self.partner_id=partner_id
        self.partner_device = None
        self.wagons_object = wagons_obj
        self.sender_wagon= None
        self.next_wagon = None
        self.wagons_list = []
        self.recent_id = uid
        self.received_id = None
        self.command_queue = []
        # self.timeout = timeout
        self.off = False
        self.GuardVan_response = False
        self.ir_message_received = False
        print(f'device created with uid: { self.originator_id} device_id: {self.device_id}  partner_id: {self.partner_id}')

    def adding_partner(self,partner):
        self.partner_device = partner
        # time.sleep(2)
        # print(f"{self.partner_device.device_id} added as partner with {self.device_id}")

    def assing_next_wagon(self,next_wagon):
        self.next_wagon = next_wagon
        # print(f"{self.next_wagon.wagon_id} assinged as next wagon with current wagon: {self.wagon_id}")

    def add_wagon(self, wagon):
        self.wagons_list.append(wagon)

    def process_command(self, command):
        if command == "LIST_ATTACHED_WAGONS":
            self.list_attached_wagons()
        else:
            self.command_queue.append(command)

    def list_attached_wagons(self):
        print(f"Engine {self.uid}: Listing attached wagons...")
        for wagon in self.wagons_list:
            print(f" - Wagon {wagon.wagon_id}")

    def send_ir_message(self):
        if(self.next_wagon!= None):
            time.sleep(2)
            print(f"Engine {self.originator_id}: Sending IR message to next Wagon")
            self.next_wagon.receive_ir_message(self,"NOACK")
            time.sleep(2)
        else:
            print(f"No Device available for {self.device_id}")

    def receive_ir_message(self, sender_wagon,type_ir):
        if(type_ir=="ACK"):
            self.ir_message_received = True
            self.sender_wagon = sender_wagon
            print(f'Engine {self.device_id}: Received an IR  message from wagon {sender_wagon.wagon_id}')
            time.sleep(2)
            # self.turn_off_send_lora()
            # self.send_wcq_lora()
        else:
            print('This is not an ACK from wagon')

    def turn_off_send_lora(self):
        print(f"Turning off Paired engine device with id: {self.partner_device.device_id}")
        time.sleep(2)
        self.partner_device.turn_off_receive_lora()

    def turn_off_receive_lora(self):
        print(f"Turnned off device with id: {self.device_id}")
        time.sleep(2)



    def send_wcq_lora(self):
        print(f"Engine {self.originator_id}: Sending WCQ via LoRa with Originator ID {self.originator_id} and Unique_id: {self.recent_id} ")
        time.sleep(2)
        for wagon in self.wagons_object:
            wagon.receive_wcq_lora(self,self.recent_id)
        # wagons_obj[0].receive_wcq_lora(self,self.recent_id)
        # wagons_obj[2].receive_wcq_lora(self,self.recent_id)
    
    def wack_receive_lora(self,sender):
            print(f"Engine {self.originator_id}: Getting WACK message from wagon_id: {sender.wagon_id} and originator_id: {sender.originator_id}")
            time.sleep(2)
            if(self.originator_id== sender.originator_id):
                self.received_id = sender.wagon_id
                self.wagons_list.append(self.received_id)
                if(sender.isGuard == True):
                    self.GuardVan_response = True
             
    def process_command(self,controlroom,command):
        if(command == "attched_wagons_list"):
            print(f"Device {self.device_id}: Received {command} command from controlroom.......")
            time.sleep(2)
            print("Sending the IR message from engine.............")
            time.sleep(2)
            self.send_ir_message()
            if(self.ir_message_received==True):
                self.turn_off_send_lora()
                while(True):
                    if(self.GuardVan_response==True):
                        print("Guard has Responded stop the process")
                        break
                    self.send_wcq_lora()
                    self.recent_id = self.received_id
                print("sending the list to control server")
                time.sleep(2)
                return [self.originator_id,self.wagons_list]
                # print("The Wagons attahed to Engine 1 are follows..............")
                # print(f'Engine E1: {Engine_2.wagons_list}')
        else:
            print("There is no other command to proceed..............")