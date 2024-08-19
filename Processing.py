# 1%
import torch
from torchvision import models, transforms
import cv2 
import numpy as np 

class ObjectTracker  :  
    def __init__(self ):  
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.device = 'cuda' if torch.cuda.is_available()   else 'cpu' 
        print("Run model on " + self.device) 
        pass

    def frameProcessing(self , frame) : 
        self.model.to(self.device)

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

class LaneDetection :    

    class PerspectiveField : 
        point1 = 0
        point2 = 0
        point3 = 0
        point4 = 0

        def clear(self) : 
            self.point1 = 0 
            self.point2 = 0 
            self.point3 = 0 
            self.point4 = 0 


    perspectiveField = PerspectiveField()  
    INITIAL = False
    
    def __init__(self) -> None: 

        def nothing(x):
            pass 

        cv2.namedWindow("Trackbars")
        cv2.createTrackbar("L - H", "Trackbars", 0, 255 , nothing)
        cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
        cv2.createTrackbar("L - V", "Trackbars", 200, 255, nothing)
        cv2.createTrackbar("U - H", "Trackbars", 255, 255, nothing)
        cv2.createTrackbar("U - S", "Trackbars", 50, 255, nothing)
        cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
        pass

    def onMouseListener(self ,event, x, y, flags, param) : 
        if event == cv2.EVENT_MOUSEMOVE :  
            # print("Mouse Move")
            pass
        if event == cv2.EVENT_LBUTTONDBLCLK : 
            # print("Mouse Click Left")
            pass
    
    def onFrame(self , frame) :    
        if frame is None : return None 
        # crop viewport!  
        # frame = cv2.line(frame , (50 ,50) , ( 200 , 200) , (255,0,0))  ]
        self.lowerHSV = np.array([
            cv2.getTrackbarPos("L - H", "Trackbars") , 
            cv2.getTrackbarPos("L - S", "Trackbars") ,
            cv2.getTrackbarPos("L - V", "Trackbars")
        ])
        self.higherHSV = np.array([
            cv2.getTrackbarPos("U - H", "Trackbars") , 
            cv2.getTrackbarPos("U - S", "Trackbars") , 
            cv2.getTrackbarPos("U - V", "Trackbars")
        ])
        w = frame.shape[1]
        h = frame.shape[0] 

        if(self.INITIAL == False) : 
            self.perspectiveField.point1 = [30 * w // 100 , 75 * h // 100] 
            self.perspectiveField.point2 = [70 * w // 100 , 75* h // 100] 
            self.perspectiveField.point3 = [16 * w // 100 , 95 * h // 100] 
            self.perspectiveField.point4 = [84 * w // 100 , 95 * h // 100] 
            self.INITIAL = True
        
        frame = cv2.GaussianBlur(frame, (7, 7), 0)
        matrix = cv2.getPerspectiveTransform(np.float32([
            self.perspectiveField.point1 , 
            self.perspectiveField.point2 , 
            self.perspectiveField.point3 , 
            self.perspectiveField.point4
        ]), np.float32([[0,0] , [w,0] , [0,h] , [w,h]]))  
        perspective = cv2.warpPerspective(frame, matrix, (w, h))

        frame = cv2.circle(frame ,self.perspectiveField.point1 , 5 , (0,0,255))
        frame = cv2.circle(frame ,self.perspectiveField.point2 , 5 , (0,255,255))

        frame = cv2.circle(frame , self.perspectiveField.point3 , 5 , (255,0,255))
        frame = cv2.circle(frame , self.perspectiveField.point4 , 5 , (255,100,255))
        
        hsv_color_frame = cv2.cvtColor(perspective, cv2.COLOR_BGR2HSV)  

        mask = cv2.inRange(hsv_color_frame , self.lowerHSV , self.higherHSV)  
        #Histogram
        histogram = np.sum(mask[mask.shape[0]//2 :, :], axis=0)
        midpoint = np.int32(histogram.shape[0]/2)
        left_base = np.argmax(histogram[:midpoint])
        right_base = np.argmax(histogram[midpoint:]) + midpoint
        
        y = h  
        lx = []
        ly = []
        
        _mask = mask.copy()


        while y > 0 :  
            img = mask[y-40:y, left_base-50:left_base+50] 
            contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
            lengthC = "" if len(contours) == 0 else len(contours)
            frame = cv2.putText(frame , "L Contours : " + str(lengthC) , (10 , 20) ,cv2.FONT_HERSHEY_SIMPLEX,.5, (0,255,0) )
            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])
                    lx.append(left_base-50 + cx)
                    left_base = left_base-50 + cx
            
            ## Right threshold
            img = mask[y-40:y, right_base-50:right_base+50]
            contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
            lengthC = "" if len(contours) == 0 else len(contours)

            frame = cv2.putText(frame , "R Contours : " + str(lengthC) , (10 , 40) ,cv2.FONT_HERSHEY_SIMPLEX,.5, (0,255,0) )

            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])
                    lx.append(right_base-50 + cx)
                    right_base = right_base-50 + cx
            
            cv2.rectangle(_mask, (left_base-50,y), (left_base+50,y-40), (255,255,255), 2)
            cv2.rectangle(_mask, (right_base-50,y), (right_base+50,y-40), (255,255,255), 2)
            y -= 40
            pass


        return {'org' : frame , 'perspective' : perspective , 'appliedRange' : mask , 'slideWindows' : _mask }