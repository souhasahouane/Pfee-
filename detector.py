from ultralytics import YOLO
from config import CONF_THRESHOLD

class PersonDetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):
        results = self.model(frame)[0]
        detections = []

        for box, cls_id, conf in zip(results.boxes.xyxy,
                                     results.boxes.cls,
                                     results.boxes.conf):

            if self.model.names[int(cls_id)] != "person":
                continue
            if conf < CONF_THRESHOLD:
                continue

            x1, y1, x2, y2 = map(int, box)
            w, h = x2 - x1, y2 - y1

            detections.append(([x1, y1, w, h], float(conf), "person"))

        return detections