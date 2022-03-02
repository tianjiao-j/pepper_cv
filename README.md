# pepper_cv
Vision tasks  
  
## Nodes

### face_detector  
Detect human faces  
```
rosrun face_detector face_detection_video.py
```

### photo_collector  
Collect photos of a person for face recognition  
**Run this first before face_recognizer**
```
rosrun photo_collector img_capture.py
```

### face_recognizer  
Recognize human faces with specific names  
**Need to run photo_collector first to get the photos of the person**
```
rosrun face_recognizer face_recog.py
```

### object_detector  
Detect objects (80 classes)  
```
rosrun object_detector yolo_obj_detection.py
```
To get the pre-trained weights:
```
wget https://pjreddie.com/media/files/yolov3.weights
```
**References**  
https://github.com/arunponnusamy/object-detection-opencv  
https://www.visiongeek.io/2018/07/yolo-object-detection-opencv-python.html



