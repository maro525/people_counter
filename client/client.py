
import argparse
from people_counter import PeopleCounter
from osc_client import Osc_Client

ID = 0

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--confidence", type=float, default=0.4,
                    help="minimum probability to filter weak detections")
    ap.add_argument("-s", "--skip-frames", type=int, default=1,
                    help="# of skip frames between detections")
    ap.add_argument("-i", "--ip", default="127.0.0.1",
                    help="OSC IP")
    ap.add_argument("-p", "--port", type=int, default=5000,
                    help="OSC PORT")
    ap.add_argument("-a", "--address", default="/people",
                    help="OSC ADDRESS")
    args = vars(ap.parse_args())

    pc = PeopleCounter(args["skip_frames"], args["confidence"])
    oc = Osc_Client(args["ip"], args["port"], args["address"])
    pc.load_video()
    while True:
        bRun = pc.run()
        send_list = [ID, pc.people_num]
        oc.send(send_list)
        if not bRun:
            break
    pc.close()
