from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]


class PeopleCounter:

    def __init__(self, skip, confidence):
        print("[INFO] loading model...")
        self.net = cv2.dnn.readNetFromCaffe(
            "./mobilenet_ssd/MobileNetSSD_deploy.prototxt", "./mobilenet_ssd/MobileNetSSD_deploy.caffemodel")
        self.skip_frames = skip
        self.confidence = confidence
        self.people_num = 0

    def load_video(self):

        print("[INFO] starting video stream...")
        self.vs = VideoStream(src=0).start()
        time.sleep(2.0)

        self.video_W = None
        self.video_H = None
        self.totalFrames = 0
        self.fps = FPS().start()

    def run(self):
        frame = self.vs.read()
        self.people_num = 0
        # frame = frame[1]

        if frame is None:
            return False

        frame = imutils.resize(frame, width=500)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if self.video_W is None or self.video_H is None:
            (self.video_H, self.video_W) = frame.shape[:2]

        if self.totalFrames % self.skip_frames == 0:
            status = "Detecting"
            self.people_num = 0
            blob = cv2.dnn.blobFromImage(
                frame, 0.007843, (self.video_W, self.video_H), 127.5)
            self.net.setInput(blob)
            detections = self.net.forward()
            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > self.confidence:
                    idx = int(detections[0, 0, i, 1])
                    if CLASSES[idx] != "person":
                        continue
                    box = detections[0, 0, i, 3:7] * np.array(
                        [self.video_W, self.video_H, self.video_W, self.video_H])
                    (startX, startY, endX, endY) = box.astype("int")
                    cx = int((startX + endX) / 2)
                    cy = int((startY + endY) / 2)
                    text = "p"
                    cv2.putText(
                        frame, text, (cx - 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.circle(
                        frame, (cx, cy), 4, (0, 255, 0), -1)
                    self.people_num += 1

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        print(self.people_num)

        if key == ord("q"):
            return False

        self.totalFrames += 1
        self.fps.update()
        return True

    def close(self):
        self.fps.stop()
        print("[INFO] elapsed time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))

        self.vs.stop()

        cv2.destroyAllWindows()
