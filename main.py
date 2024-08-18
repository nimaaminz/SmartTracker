# 1%  
from CameraInterface import *  
from Processing import ObjectTrackerYOLO
from threading import Thread

RUN = True  

if __name__ == '__main__':        
    cameraInterface1 = CameraInterface(0)  
    objectTrackerYOLO = ObjectTrackerYOLO() 
    def onFrameReceive(frame) :  
        cv2.imshow("main" , frame)  

    def commandLineSystem() :  

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
                case "?" : 
                    print("""
                            not for now
                          """)
                case _ : 
                    if len(cmd) > 0 : 
                        print("unknown command") 


    Thread(target=commandLineSystem).start()


    cameraInterface1.start_camera(onFrameReceive) 
    cv2.destroyAllWindows()

    pass 