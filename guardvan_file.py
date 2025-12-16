import time
class GuardVan():
    def __init__(self, device_id,partner_id,uid):
        self.wagon_id = uid
        self.device_id = device_id
        self.originator_id = None
        self.partner_id = partner_id
        self.ir_message_received = False
        self.isGuard = True
        self.sender_wagon= None
        self.next_wagon = None
        self.partner_device = None
        print(f'device created with uid: { self.wagon_id} device_id: {self.device_id}  partner_id: {self.partner_id}')


    def adding_partner(self,partner):
        self.partner_device = partner
        # time.sleep(2)
        # print(f"{self.partner_device.device_id} added as partner with {self.device_id}")

    def receive_ir_message(self, sender_wagon,type_ir):
            self.ir_message_received = True
            self.sender_wagon = sender_wagon
            self.originator_id = sender_wagon.originator_id
            time.sleep(2)
            print(f'Device {self.device_id}: Received IR message with originator_id: {sender_wagon.originator_id} and device_id: {sender_wagon.device_id}')
            time.sleep(2)
            self.send_ack_ir(sender_wagon)
            time.sleep(2)

    def send_ack_ir(self,sender_wagon):
        print(f"Device {self.device_id}: Sending ACK Back via IR.")
        time.sleep(2)
        sender_wagon.receive_ir_message(self,'ACK')

    def send_wack_lora(self,sender):
        print(f"Device {self.device_id}: Sending WACK via LoRa with Wagon ID: {self.wagon_id} and Originator ID: {self.originator_id}.")
        sender.wack_receive_lora(self)
        time.sleep(2)

    def receive_wcq_lora(self, sender,uid):
        new_originator_id = sender.originator_id
        print(f"Device {self.device_id}: Received WCQ message with originator_id {new_originator_id}")
        time.sleep(2)
        if(self.originator_id==new_originator_id and self.ir_message_received==True and self.wagon_id != uid):
             self.send_wack_lora(sender)
        else:
            print(f"Device {self.device_id}: Discarded the LoRa message")
            time.sleep(2)

    def turn_off_send_lora(self):
        print(f"Turning off Paired engine device with id: {self.partner_device.device_id}")
        time.sleep(2)
        self.partner_device.turn_off_receive_lora()

    def turn_off_receive_lora(self):
        print(f"Turnned off device with id: {self.device_id}")
        time.sleep(2)