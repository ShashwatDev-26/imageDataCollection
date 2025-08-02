import cv2
import time
import os
import json

class detectionDataCollection:

  def __init__(self,rootDir="train"):
    self.__rootDir         = os.path.join(os.getcwd(),"detectionDataset",rootDir)
    self.__imagePath       = None
    self.__labelsPath      = None

    self.__sourceID        = None
    self.__cap             = None
    self.__camera_flag     = False
    self.__height          = None
    self.__width           = None

    self.__drawing         = False
    self.__startCood       = None
    self.__endCood         = None

    self.__classes         = dict()
    self.__name            = None
    self.__classindex      = None

    self.__coordinates     = list()
    self.__bound           = False

    self.__StartTime       = False
    self.__Timer           = None

    self.__nSamples         = None
    self.__cSample          = None


    self.set_sourceID()
    self.set_Timer(5)
    self.set_frameHight()
    self.set_frameWidth()
    self.set_nSamples()

  def set_sourceID(self,ID=0):
     self.__sourceID=ID
  def set_Timer(self,time=-1):
      self.__Timer = time
  def set_frameHight(self,height=480):
      self.__height = height
  def set_frameWidth(self,width=640):
      self.__width = width
  def set_nSamples(self,sample=50):
      self.__nSamples = sample
  def get_json(self):
    file_path = os.path.join(self.__rootDir,"nclasses.json")
    with open(file_path, "w") as json_file:
        json.dump(self.__classes, json_file, indent=4) # indent for pretty printing


  def get_classes(self):
      return self.__classes


  def __structdir(self):
    self.__imagePath  = os.path.join(self.__rootDir,"images")
    self.__labelsPath = os.path.join(self.__rootDir,"labels")
    os.makedirs(self.__imagePath,exist_ok=True)
    os.makedirs(self.__labelsPath,exist_ok=True)
    prompt=f"""
    ****************************************************************************
                                  Directory structure
    ****************************************************************************

|->  {self.__rootDir}
    |-> {self.__imagePath}
    |-> {self.__labelsPath}


    """
    print(prompt)

  def __classupdate(self):

      self.__name = str(input("Enter the class name: ")).strip().lower().replace(" ","_")

      if self.__name == "":
          print("[*] No Update...")
          return False
      elif self.__name not in self.__classes:
          self.__classindex = self.__classes[self.__name]  = len(self.__classes)
          return True
      elif self.__name in self.__classes:
          self.__classindex = self.__classes[self.__name]
          return True

  def __coordinate(self):
      """
            Coordinates: self.__classindex,x_center,y_center,width,height
      """

      x1 =    min(self.__startCood[0],self.__endCood[0])
      y1 =    min(self.__startCood[1],self.__endCood[1])
      x2 =    max(self.__endCood[0],self.__endCood[0])
      y2 =    max(self.__endCood[1],self.__endCood[1])

      x_center    =      (x1 + x2) / 2 / self.__width
      y_center    =      (y1 + y2) / 2 / self.__height

      width       =      (x2 - x1) / self.__width
      height      =      (y2 - y1) / self.__height

      coord =   (self.__classindex,x_center,y_center,width,height)

      self.__coordinates.append(coord)
      self.__startCood   = False
      self.__endCood     = False

  def __drawRect(self,event, x, y, flags, param):


      if event == cv2.EVENT_LBUTTONDOWN and (flags & cv2.EVENT_FLAG_CTRLKEY):
            self.__drawing     = True
            self.__startCood   = (x,y)
      elif event == cv2.EVENT_MOUSEMOVE and self.__drawing:
            self.__endCood = (x,y)
      elif event == cv2.EVENT_LBUTTONUP and self.__drawing:
          self.__drawing   = False
          self.__endCood   = (x,y)
      elif event == cv2.EVENT_RBUTTONDOWN and self.__StartTime == False:
            if self.__endCood and self.__startCood:
                update = self.__classupdate()
                if update:
                    self.__coordinate()
                    self.__bound = True
                else:
                    self.__endCood   = False
                    self.__startCood = False

      if event == cv2.EVENT_RBUTTONDOWN and (flags & cv2.EVENT_FLAG_CTRLKEY) and self.__bound:
          self.__StartTime = time.time()
          self.__bound   = False




  def camera_init_(self,):
        """
            sourceID     : int >= 0 , proper url with usrseName and password if applicable Default 0
            (int) height : Hight of the Frame, Default: 480px
            (int) width  : Width of the Frame, Default: 640px
        """

        if self.__sourceID is None:
            print("[*] Camera must be initiated with Source ")
            return

        self.__cap = cv2.VideoCapture(self.__sourceID)

        if not self.__cap.isOpened():
            print("[*] Error: Unable to open camera! .")
            return
        else:
            self.__camera_flag = True
            self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.__width)
            self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__height)
            print(f"[*] Camera is initiating with Source-ID: {self.__sourceID}")

  def annotation(self):

     ctime            = 0
     msg              = ""
     classlen         = 0
     capture_block    = False

     if self.__camera_flag:
        print("[*] Camera is initiated successfully.")
        self.__structdir()
        cv2.namedWindow("Live")
        cv2.setMouseCallback("Live",self.__drawRect)
     else:
        print("[*] Camera is not initiated...")
        return

     while(True):
        ret,Frame=self.__cap.read()

        if not ret:
                print("[*] Frame not found! ")
                break
        else:
            Frame       = cv2.flip(Frame,1)
            mod_frame   = Frame.copy()

        if self.__endCood and self.__startCood:
            Sx = min(self.__startCood[0],self.__endCood[0])
            Sy = min(self.__startCood[1],self.__endCood[1])
            Ey = max(self.__startCood[1],self.__endCood[1])
            msgadd   = "[*] RIGHT CLILCK TO +ADD OBJECT: "
            msgcoord = "[*] CTRL + RIGHT CLICK TO CAPTURE:"
            cv2.putText(mod_frame,msgadd,(Sx+2,Sy-2),1,1,(0,128, 255),2,4)
            cv2.putText(mod_frame,msgcoord,(Sx+2,Ey+11),1,1,(0,128, 255),2,4)
            cv2.rectangle(mod_frame,self.__startCood,self.__endCood,(255,23,4),1)



        if self.__StartTime:
            ctime = int(time.time()-self.__StartTime)
            msg   = f"[*] {ctime:02}:00"
            cv2.putText(mod_frame,msg,(10,50),1,1,(128,0, 255),2,4)
        if ctime > self.__Timer:
            self.__StartTime = False
            capture_block    = True
            self.__cSample   = len(os.listdir(self.__imagePath))
            classlen         = len(self.__coordinates)
            if self.__cSample != 0:
                self.__nSamples+=self.__cSample
            ctime = 0


        if capture_block:
            if self.__cSample < self.__nSamples:
                msg = f"[{self.__cSample}] capturing..."
                cv2.putText(mod_frame,msg,(10,59),1,0.9,(255,128, 1),1,4)
                img = os.path.join(self.__imagePath, f'frame_{classlen:03}_{self.__cSample:03}.jpg')
                lab = os.path.join(self.__labelsPath, f'frame_{classlen:03}_{self.__cSample:03}.txt')

                # print(f'\n[*] frame_{classlen:03}_{self.__cSample:03}.jpg')

                cv2.imwrite(img, Frame)
                with open(lab,'w') as file:
                        for i in range(classlen):
                            #  classindex,x_center,y_center,width,height
                            classindex,x_center,y_center,width,height = self.__coordinates[i]
                            if i == classlen-1:
                                file.write(f'{classindex} {x_center} {y_center} {width} {height}')
                            else:
                                 file.write(f'{classindex} {x_center} {y_center} {width} {height}\n')

            else:
                self.__coordinates=[]
                capture_block = False

            self.__cSample+=1

        cv2.imshow("Live",mod_frame)

        if cv2.waitKey(1)==27:
           print("[*] Stopped by user ")
           break
     self.__cap.release()
     cv2.destroyAllWindows()


class classificationDataCollection:
    def __init__(self,collectiondir="train"):
        self.collectiondir        = collectiondir
        self.__rootdir            = None
        self.__classID            = dict()
        self.classPath            = None
        self.currentFileName      = None

        self.__cap                = None
        self.__sourceID           = None
        self.__camera_flag        = False

        self.__startCood          = None
        self.__endCood            = None
        self.__drawing            = False

        self.__capture            = False
        self.__samples            = None
        self.__timer              = None
        self.__start_timer        = False
        self.__Framecount         = None


        self.__dirStruct()
        self.set_timer()
        self.set_semples()
        self.set_SourceID()

    def set_SourceID(self,sourceID=0):
        self.__sourceID=sourceID
    def set_semples(self,samples=10):
        self.__samples = samples
    def set_timer(self,timer=5):
        self.__timer = timer
    def set_nameOfObject(self,name):
        self.currentFileName=name
    def get_ClassID(self,name=None):
        if name in list(self.__classID.keys()):
            return self.__classID[name]
        return self.__classID

    def __dirStruct(self):
        self.__rootdir = os.path.join(os.getcwd(),"classificationDataset",self.collectiondir)
        # print(self.__rootdir)
        os.makedirs(self.__rootdir,exist_ok=True)
        return self.__rootdir
    def __classupdate(self):
        self.currentFileName = str(input("[*] Enter the Object name: ")).strip().lower().replace(" ","_")
        dL1=len(self.__classID)
        self.__classID[self.currentFileName]=dL1
        if dL1 == len(self.__classID):
            print("[*] Object already exist: ")

            self.__Framecount = len(os.listdir(self.classPath))
            if self.__Framecount!=0:
                self.__samples+=self.__Framecount
        else:
            self.classPath = os.path.join(self.__rootdir,self.currentFileName)
            os.makedirs(self.classPath,exist_ok=True)

            self.__Framecount = len(os.listdir(self.classPath))

    def camera_init_(self,height=480,width=640):
        """
            sourceID     : int >= 0 , proper url with usrseName and password if applicable Default 0
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

    def __drawRect(self,event, x, y, flags, param):

       if event == cv2.EVENT_LBUTTONDOWN:
           self.__drawing     = True
           self.__start_timer = False
           self.__startCood   = (x,y)
       elif event == cv2.EVENT_MOUSEMOVE:
           if self.__drawing:
               self.__endCood = (x,y)
       elif event == cv2.EVENT_LBUTTONUP:
           self.__drawing   = False
           self.__endCood   = (x,y)
       elif event == cv2.EVENT_RBUTTONDOWN:
           self.__classupdate()
           self.__start_timer  = time.time()
           self.__drawing      = False



    def imageCropingAndCapturing(self):
        msgcoordinat = ""
        msgCapturing = ""

        if self.__camera_flag == False:
            print("[*] Camera is not initiated...")
            return
        else:
            # cv2.namedWindow("Main_window")
            cv2.namedWindow("instruct_window")
            cv2.setMouseCallback("instruct_window",self.__drawRect)

        while(True):
            ret,Frame = self.__cap.read()

            if not ret:
                print("[*] Frame is Not working")
                break
            else:
                Frame       = cv2.flip(Frame,1)
                mod_frame   = Frame.copy()

            if self.__endCood and self.__startCood:

                tx,ty = self.__startCood
                msgcoordinat   = "[*] RIGHT CLILCK TO +ADD: "

                cv2.putText(mod_frame,msgcoordinat,(tx+2,ty-2),1,0.9,(0,128, 255),2,4)
                cv2.rectangle(mod_frame,self.__startCood,self.__endCood,(255,23,4),1)
            if self.__start_timer:
                timer = int(time.time()-self.__start_timer)
                msg =f"[*] {timer:02}:00"
                cv2.putText(mod_frame,msg,(10,50),1,0.9,(0,128, 255),1,4)
                if timer>self.__timer:
                    msgCapturing = "[*] Capturing Started..."
                    cv2.putText(mod_frame,msgCapturing,(10,50),1,0.9,(0,0, 255),1,4)
                    self.__start_timer = False
                    self.__capture     = True

            if self.__capture:
                if self.__Framecount<self.__samples:
                    x1,y1  = self.__startCood
                    x2,y2  = self.__endCood

                    # Ensure ROI is within frame bounds
                    x1 = max(x1, 0)
                    y1 = max(y1, 0)
                    x2 = min(x2, mod_frame.shape[1])
                    y2 = min(y2, mod_frame.shape[0])

                    cropped = mod_frame[y1:y2, x1:x2]
                    if cropped.size != 0:
                        cv2.imshow("Cropped Video", cropped)
                    msgCapturing = f"{self.__classID[self.currentFileName]:03}_{self.__Framecount:03}"
                    filepath= os.path.join(self.classPath,msgCapturing+".jpg")
                    cv2.imwrite(filepath,cropped)
                    cv2.putText(mod_frame,msgCapturing,(10,50),1,0.9,(0,255, 0),1,4)

                else:
                    self.__capture      = False
                    self.__startCood    = None
                    self.__endCood      = None

                    msgCapturing = f"[*] Capturing Done of {self.__Framecount:03}s Frames"
                    cv2.putText(mod_frame,msgCapturing,(10,50),1,0.9,(0,255, 0),1,4)
                    print(msgCapturing)

                self.__Framecount+=1






            # cv2.imshow("Main_window",Frame)
            cv2.imshow("instruct_window",mod_frame)
            if cv2.waitKey(1)==27:
                print("[*] Stopped by User")
                break

        self.__cap.release()
        cv2.destroyAllWindows()










