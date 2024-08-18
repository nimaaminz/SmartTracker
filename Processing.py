# 1%
import torch
from torchvision import models, transforms 
import cv2 

class ObjectTracker  :  
    def __init__(self ):  
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.device = 'cuda' if torch.cuda.is_available()   else 'cpu' 
        print("Run model on " + self.device) 
        pass

    def frameProcessing(self , frame) : 
        self.model.to(self.device)
        # frame = [frame]
        results = self.model(frame) 
        labels, cord = results.xyxyn[0][:, -1].cpu().numpy(), results.xyxyn[0][:, :-1].cpu().numpy()

        # plot 
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.2:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 1) 
                cv2.putText(frame, self.model.names[int(labels[i])], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 1)

        return frame

    pass