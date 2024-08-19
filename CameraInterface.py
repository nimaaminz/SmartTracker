import cv2 
import numpy as np 

class Event:
    def __init__(self): self.listeners = []
    def register_listener(self, listener): self.listeners.append(listener)
    def notify(self, *args):
        for listener in self.listeners: listener(*args)

class CameraInterface :  
    # private 
    _run_cam = True  
    cameraPropertiesWindow = True 

    def __init__(self ,cam_index ) -> None: 
        self.videoCapture = cv2.VideoCapture(cam_index)
        pass

    def exposure(self , value = None) :  
        if self.videoCapture is not None and value is not None: 
            self.videoCapture.set(cv2.CAP_PROP_EXPOSURE , int(value))  
        else :
            return self.videoCapture.get(cv2.CAP_PROP_EXPOSURE) 
        pass
    def contrast(self , value = None) : 
        if self.videoCapture is not None and value is not None: 
            self.videoCapture.set(cv2.CAP_PROP_CONTRAST , int(value))  
        else :
            return self.videoCapture.get(cv2.CAP_PROP_CONTRAST) 
    def brightness(self , value = None) : 
        if self.videoCapture is not None and value is not None: 
            self.videoCapture.set(cv2.CAP_PROP_BRIGHTNESS , int(value))  
        else :
            return self.videoCapture.get(cv2.CAP_PROP_BRIGHTNESS)  
    def saturation(self , value = None) : 
        if self.videoCapture is not None and value is not None: 
            self.videoCapture.set(cv2.CAP_PROP_SATURATION , int(value))  
        else :
            return self.videoCapture.get(cv2.CAP_PROP_SATURATION)  
    def hue(self , value = None) : 
        if self.videoCapture is not None and value is not None: 
            self.videoCapture.set(cv2.CAP_PROP_HUE, int(value))  
        else :
            return self.videoCapture.get(cv2.CAP_PROP_HUE )  
        

    def fps(self) : 
        if self.videoCapture is not None : 
            return self.videoCapture.get(cv2.CAP_PROP_FPS) 
        
    
    def start_camera(self , callback) :  
        while self._run_cam :
            ret , frame = self.videoCapture.read()  
            if ret == True :    
                if callback is not None : 
                    callback(frame)
            if ret == False or (cv2.waitKey(1) & 0xFF == ord('q')): break
    
    def pause(self) : 
        self._run_cam = False 
    
    
    def cameraCalibratoin (self , frame) :    
        found, corners = cv2.findChessboardCorners(frame , (7,7), cv2.CALIB_CB_ADAPTIVE_THRESH)  
        if found : 
            cv2.drawChessboardCorners(frame, (7,7), corners, found)
            cv2.imshow('img_captured_corners', frame) 
        return frame
        pass


    def printCalibration(self , r = 640) :   
        patternBitmap = np.zeros((r , r , 3) , np.uint8)     
        step = r // 10 
        j = 0 
        i = 0 
        for j in range(0, r, step):
            for i in range(0, r, step):
                if (i // step + j // step) % 2 == 0:
                    color = (255, 255, 255)
                else :
                    color = (0, 0, 0)
                cv2.rectangle(patternBitmap, (i, j), (i + step, j + step), color, -1)
        return patternBitmap  

