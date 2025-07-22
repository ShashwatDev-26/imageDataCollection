import cv2
import time
import os
class detectionDataCollection:

    def __init__(self,save_dir='train'):
        self.__cap             =  None
        self.__drawing         =  False
        self.__start_time      =  False
        self.save_dir          =  save_dir
        self.__frame_count     =  0
        self.__record_msg      =  "[*] Single Mode is on."

        self.__rect_end        =  None
        self.__rect_start      =  None
        self.__sourceID        =  None

        self.__coordinate_flag =  False
        self.__camera_flag     =  False
        self.__coordinatesli   =  []
        self.classDict         =  dict()

        self.set_SourceID(0)
        self.set_timer(5)
        self.set_Frame_cap(10)
        self.set_multiAnotation(False)

    # All Setters
    def set_SourceID(self,sourceID):
        self.__sourceID=sourceID
    def set_timer(self,timer):
        self.__timer=timer
    def set_Frame_cap(self,Ncap):
        self.__Frame_cap=Ncap
    def set_multiAnotation(self,mult):
        self.__record_msg  = "[*] Multi Mode is ON."
        self.__multi = mult

    # Private Methods
    def __set_coordinate(self,classlen=0,w=0,h=0):
        if self.__coordinate_flag:
            RoiX1,RoiY1 = self.__rect_start
            RoiX2,RoiY2 = self.__rect_end
            self.__coordinatesli.append([classlen,RoiX1,RoiY1,RoiX2,RoiY2,w,h])
            self.__coordinate_flag = False

    def __updateClass(self):
        k = str(input("[*] Enter the name of object: ")).lower().strip().replace(" ","_")
        if k=="":
            print("[*] No Update")
            return False
        elif k not in self.classDict:
            self.classDict[k] = len(self.classDict)
            return True
    def __draw_rectangle(self,event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.__drawing     = True
            self.__rect_start  = (x, y)


        elif event == cv2.EVENT_MOUSEMOVE:
            if self.__drawing:
                self.__rect_end = (x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            self.__drawing         = False
            self.__rect_end        = (x, y)
            self.__frame_count     = 0
            self.__update          = self.__updateClass()

            if self.__update:
                self.__coordinate_flag = True
                self.__start_time      = time.time()
                print("[*] Class updated ...")
            else:
                print("[*] No new class is Added.. ")


            if self.__multi:
                Toggle = input("[*] Continue on Adding classes (Y/N): ").lower().strip()[0]
                if Toggle =="y":
                    self.__multi       = True
                else:
                    self.__record_msg  ="[*] Single Mode is on."
                    print("[*] Capturing is on Process.")
                    print(f"[*] Wait for{self.__timer}s")
                    self.__multi           = False
                    self.__start_time      = time.time()
                    self.__update          = True

    def __Directories(self):
        """
            return: images_path, labels_path
        """
        imgf = os.path.join(self.save_dir,"images")
        labf = os.path.join(self.save_dir,"labels")
        os.makedirs(imgf,exist_ok=True)
        os.makedirs(labf,exist_ok=True)
        return imgf,labf

    # Camera Init
    def camera_init_(self,height=480,width=640):


        """
            sourceID : int >= 0 , proper url with usrname and password if applicable Default 0
            (int) height : Hight of the Frame, Default: 480px
            (int) width  : Width of the Frame, Default: 640px
        """

        if self.__sourceID is None:
            print("[*] Camera must be initiated with Source ")
            return

        self.__cap = cv2.VideoCapture(self.__sourceID)

        if not self.__cap.isOpened():
            print("[*] Error: Could not camera stream.")

        else:
            self.__camera_flag = True
            self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            print(f"[*] Camera is initialised with Source-ID: {self.__sourceID}")

    # Main Mathod
    def annotation(self):

        """
            (str) save_dir  : It will create a Directory, if not exist,         |*| Default: None
            (int) timer     : Timer for Wait time after creating a bounding box |*| Default: 5s
            (int) Frame_cap : Number of frame you want to capture. After timer  |*| Default: 30
        """

        imgpath = None
        labpath = None
        if self.save_dir is None:
            print("invalid Directory! ")
            return
        else:
            imgpath,labpath = self.__Directories()
        # variable __init
        self.__rect_start     =  None
        self.__rect_end       =  None
        self.__coordinatesli  =  []
        self.__start_time     =  False
        self.__frame_count    =  0


        # Initialize camera frame
        if self.__camera_flag == False:
            print("[*] Camera is not initiated...")
            return

        cv2.namedWindow("instruction")
        cv2.setMouseCallback("instruction", self.__draw_rectangle)

        while True:
            ret, frame  = self.__cap.read()
            if not ret:
                break
            frame       = cv2.flip(frame,1)
            mod_frame   = frame.copy()


            # If drawing or after mouse released
            if self.__rect_start and self.__rect_end:
                cv2.rectangle(mod_frame, self.__rect_start, self.__rect_end, (0, 0, 255), 1)

            # Only for multi-Annotation
            if self.__multi:
                self.__start_time = False
                classlen          = len(self.classDict)-1
                self.__set_coordinate(frame.shape[0],frame.shape[1])

            if self.__start_time and (time.time() - self.__start_time) >= self.__timer:

                # Flag is on from release_left_button
                classlen       = len(self.classDict)
                self.__set_coordinate(classlen,frame.shape[0],frame.shape[1])


                if self.__frame_count < self.__Frame_cap and self.__update:

                    length = len(self.__coordinatesli)
                    self.__record_msg = f"[*] Capturing Frame: {self.__frame_count}"
                    img = os.path.join(imgpath, f'frame_{classlen}_{self.__frame_count:03}.jpg')
                    lab = os.path.join(labpath, f'frame_{classlen}_{self.__frame_count:03}.txt')

                    cv2.imwrite(img, frame)

                    with open(lab,'w') as file:
                        for i in range(length):
                            cl,RoiX1,RoiY2,RoiX2,RoiY2,W,H = self.__coordinatesli[i]
                            if i == length-1:
                                file.write(f'{classlen} {RoiX1} {RoiY2} {RoiX2} {RoiY2} {W} {H}')
                            else:
                                file.write(f'{classlen} {RoiX1} {RoiY2} {RoiX2} {RoiY2} {W} {H}\n')
                    print(f"[*] Saved {img}")
                    self.__frame_count+=1

                else:
                    self.__start_time     =  False
                    self.__coordinatesli  =  []
                    self.__record_msg            =  f"[*] Capturing completed.. "

            cv2.putText(mod_frame, self.__record_msg, (10, 50),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

            cv2.imshow("instruction",mod_frame)
            # cv2.imshow("Draw Rectangle", frame)  # uncomment to see original capture image

            if cv2.waitKey(1) & 0xFF == 27:        # Press ESC to exit
                print("[*] Capturing Stopped...! ")
                break

        self.__cap.release()
        cv2.destroyAllWindows()

    def HowToUse(self):
        """
        >> test.detectionDataCollection("dir_name") |*| default: train

        # User Settings are
        <-- test the camera befor seting Source id -->
        >> test.set_SourceID(int/url)         |*| default: 0
        >> test.set_timer(int)                |*| default: 5
        <-- Number of samples -->
        >> test.set_Frame_cap(int)            |*| default: 10
        >> test.set_multiAnotation(False)     |*| default: False

        # Main Functions
        test.camera_init_(height,width)       |*| default: height=480,width=640
        test.annotation()
        ########################################################################
                                        Instruction
        ########################################################################

        >> Single mode <<
        [*] test.detectionDataCollection("train")
        [*] test.set_multiAnotation(True)
        [*] test.camera_init_()
        [*] test.annotation()

        story:
        ''''''


        >> Multi mode <<
        [*] test.detectionDataCollection("train")
        [*] test.set_multiAnotation(True)
        [*] test.camera_init_()
        [*] test.annotation()

        story:
        ''''''



        """









