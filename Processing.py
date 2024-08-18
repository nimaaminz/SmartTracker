# 1%
from ultralytics import YOLO

class ObjectTrackerYOLO : 
    def __init__(self, model_path="yolov8n.pt"): 
        self.model = YOLO(model_path)
        pass
    pass