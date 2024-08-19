# 1%  
from CameraInterface import *  
from Processing import ObjectTracker , LaneDetection
from threading import Thread

RUN = True  
OBJECT_DETECTION_PROCESS_ACTIVATION = True  

if __name__ == '__main__':        

    cameraInterface1 = CameraInterface(0)  
    objectTracker = ObjectTracker()  
    laneDetection = LaneDetection()

    def onFrameReceive(frame) :   
        global OBJECT_DETECTION_PROCESS_ACTIVATION
        _frame = frame 
        if OBJECT_DETECTION_PROCESS_ACTIVATION : 
            frame = objectTracker.frameProcessing(frame) 
        processedFrame = laneDetection.onFrame(_frame)   
        cv2.imshow("Perspective" , processedFrame['perspective'])  
        cv2.imshow("appliedRange" , processedFrame['appliedRange'])   
        cv2.imshow("slideWindows" , processedFrame['slideWindows'])   
        cv2.imshow("main" , frame)  

    def commandLineSystem() :  
        global OBJECT_DETECTION_PROCESS_ACTIVATION
        def isNumeric(s : str) : 
            if s.startswith('-'):
                s = s[1:] 
            return s.isdigit()
        

        commandLineLock = False  
        while RUN and commandLineLock == False : 
            
            cmd = input(">>").strip()
            match cmd :  
                case "cam props" :  
                    active = True  
                    while active : 
                        _cmd = input(">>CameraProperties>>").strip()
                        match _cmd : 
                            case "brightness -s" :  
                                value = input("Enter a single number: ").strip()
                                if isNumeric(value) == False:  
                                    print("insert number only") 
                                else :
                                    cameraInterface1.brightness(value)
                                    print(cameraInterface1.brightness())

                            case "brightness" :  
                                print(cameraInterface1.brightness())  


                            case "contrast -s" :  
                                value = input("Enter a single number: ").strip()
                                if isNumeric(value) == False:  
                                    print("insert number only") 
                                else :
                                    cameraInterface1.contrast(value)
                                    print(cameraInterface1.contrast())

                            case "contrast" :  
                                print(cameraInterface1.contrast())  

                            case "saturation -s" :  
                                value = input("Enter a single number: ").strip()
                                if isNumeric(value) == False:  
                                    print("insert number only") 
                                else :
                                    cameraInterface1.saturation(value)
                                    print(cameraInterface1.saturation())

                            case "saturation" :  
                                print(cameraInterface1.saturation())  

                            case "hue -s" :  
                                value = input("Enter a single number: ").strip()
                                if isNumeric(value) == False:  
                                    print("insert number only") 
                                else :
                                    cameraInterface1.hue(value)
                                    print(cameraInterface1.hue())

                            case "hue" :  
                                print(cameraInterface1.hue())  

                            case "exposure -s" :  
                                value = input("Enter a single number: ").strip()
                                if isNumeric(value) == False:  
                                    print("insert number only") 
                                else :
                                    cameraInterface1.exposure(value)
                                    print(cameraInterface1.exposure())

                            case "exposure" :  
                                print(cameraInterface1.exposure())
                            case "fps" : 
                                print(cameraInterface1.fps()) 
                            case "back" : 
                                active = False
                            case _ : 
                                if len(_cmd) > 0 : 
                                    print("unknown command") 
                                    
                    pass # CAMERA PROPERTIES 
                case "detection":  
                    value = input('value * 1|0 : ').strip()
                    if isNumeric(value) == False: 
                        print("Invalid input")
                    else :  
                      OBJECT_DETECTION_PROCESS_ACTIVATION = bool(int(value))
                    pass    
                case "?" : 
                    print(f"""
                        Available commands:
                        ------------------------------------------------------------------------------------------
                        cam props: Adjust camera properties (brightness, contrast, saturation, hue, exposure, fps)
                        detection: Enable or disable object detection (1 to enable, 0 to disable)
                          """)
                case _ : 
                    if len(cmd) > 0 : 
                        print("unknown command") 


    Thread(target=commandLineSystem).start()


    cameraInterface1.start_camera(onFrameReceive) 
    cv2.destroyAllWindows()

    pass 