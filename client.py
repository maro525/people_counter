
import argparse
from people_counter import PeopleCounter
from osc_client import Osc_Client
from cameraname import get_camera_name

pcs = []  # array of people counter class


def set_camera_name():
    return get_camera_name('USB')


def main(skip_frame, confidence, osc_ip, osc_port, osc_address):
    for i in range(3):
        pc = PeopleCounter(skip_frame, confidence)
        pcs.append(pc)

    oc = Osc_Client(osc_ip, osc_port, osc_address)

    cam_indexes = get_camera_name('USB')
    if len(cam_indexes) is 0:
        print("[CAM GET ERROR] no usb camera")
        return

    for i, pc in enumerate(pcs):
        pc.load_video(cam_indexes[i])

    while True:
        bRun = True
        for i, pc in enumerate(pcs):
            bCamera_running = pc.run()
            if bCamera_running is False:
                print("camera", i, "not running")
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
