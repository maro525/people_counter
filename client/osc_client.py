from pythonosc import osc_message_builder
from pythonosc import udp_client


class Osc_Client:

    def __init__(self, ip, port, address):
        self.client = udp_client.UDPClient(ip, port)
        self.address = address

    def send(self, send_list):
        msg = osc_message_builder.OscMessageBuilder(address=self.address)
        for i in send_list:
            msg.add_arg(i)
        msg = msg.build()
        self.client.send(msg)
