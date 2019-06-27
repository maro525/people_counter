
import argparse
from people_counter import PeopleCounter

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--confidence", type=float, default=0.4,
                    help="minimum probability to filter weak detections")
    ap.add_argument("-s", "--skip-frames", type=int, default=1,
                    help="# of skip frames between detections")
    args = vars(ap.parse_args())

    pc = PeopleCounter(args["skip_frames"], args["confidence"])
    pc.load_video()
    pc.run()
