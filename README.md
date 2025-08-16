# <center>🎥Image Data Collection</center>

## Instructions For Detection Data.

***

* To create a bounding box around an object, press and hold **Ctrl** while simultaneously pressing the **left mouse button**. Drag the cursor to encompass the desired object within the box.

* To assign a name to the object, **right-click** within the bounding box. Alternatively, repeat the bounding box creation process as described above.

* Enter the object's name in the console and press **Enter** to confirm.

* Multiple objects can be labeled sequentially by repeating the aforementioned steps for each object.

* Initiate the timer by pressing and holding **Ctrl** while **right-clicking**.

* Please note that once image capture has commenced, redrawing bounding boxes is disabled until the capture process is complete.
* To terminate the process, press the Esc key.

### init code
***
~~~
from Data_Collection import detectionDataCollection
if __name__ == __main__:
  dtest = detectionDataCollection()
  dtest.set_sourceID(0)
  dtest.set_nSamples(1)
  dtest.set_Timer(5)
  dtest.camera_init_()
  dtest.annotation()
~~~
***
![](https://github.com/ShashwatDev-26/imageDataCollection/blob/main/media/Demo_DataDetection.gif)
***

## Instructions for Classification Data
***
*   To designate an object, **left-click** and drag the cursor to create a bounding box encompassing the desired item.
*   **Right-click** within the bounding box to input the object's name.
*   Upon pressing **Enter**, the data acquisition timer will commence.
*   Data capture will proceed for the specified number of samples.
*   To terminate the process, press the **Esc** key.

### init code
***
~~~
from Data_Collection import classificationDataCollection
if __name__ == __main__:
  path = "..\src\Test.mp4"
  test = classificationDataCollection()
  test.set_SourceID(0) # | test.set_SourceID(path)
  test.set_playback_speed(15)
  test.set_semples(1)
  test.set_timer(5)
  test.camera_init_()
  test.imageCropingAndCapturing()
~~~
***
![](https://github.com/ShashwatDev-26/imageDataCollection/blob/main/media/Demo_DataClassificaton.gif)

***
# <center> To be continued ....</center>

***
