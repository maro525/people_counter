import argparse


class Osc_Server:

    def __init__(self, ip, port, address):
        self.ip = ip
        self.port = port
        self.address = address

    def start(self):
        from pythonosc import dispatcher
        from pythonosc import osc_server
        dispatcher = dispatcher.Dispatcher()
        dispatcher.map(self.address, print)
        server = osc_server.ThreadingOSCUDPServer(
            (self.ip, self.port), dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=5000, help="The port to listen on")
    parser.add_argument("--address",
                        default="/people",
                        help="the address to listen on")

    args = parser.parse_args()

    os = Osc_Server(args.ip, args.port, args.address)
    os.start()
