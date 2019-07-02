
import argparse
from people_counter import PeopleCounter
from osc_client import Osc_Client

camera_ids = [0, 1, 2]
pcs = []  # array of people counter class


def main(skip_frame, confidence, osc_ip, osc_port, osc_address):
    for i in range(3):
        pc = PeopleCounter(camera_ids[0], skip_frame, confidence)
        pcs.append(pc)

    oc = Osc_Client(osc_ip, osc_port, osc_address)

    for pc in pcs:
        pc.load_video()

    while True:
        bRun = True
        for pc in pcs:
            bCamera_running = pc.run()
            if not bCamera_running:
                bRun = False
                break

        # if camera not working, break
        if not bRun:
            break

        # send osc
        for pc in pcs:
            send_list = [pc.cam_num, pc.people_num]
            oc.send(send_list)

    for pc in pcs:
        pc.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--confidence", type=float, default=0.4,
                    help="minimum probability to filter weak detections")
    ap.add_argument("-s", "--skip-frames", type=int, default=3,
                    help="# of skip frames between detections")
    ap.add_argument("-i", "--ip", default="127.0.0.1",
                    help="OSC IP")
    ap.add_argument("-p", "--port", type=int, default=5000,
                    help="OSC PORT")
    ap.add_argument("-a", "--address", default="/people",
                    help="OSC ADDRESS")
    args = vars(ap.parse_args())

    main(args["skip_frames"], args["confidence"],
         args["ip"], args["port"], args["address"])
