# pepper_cv
Vision tasks  
  
## Nodes

### face_detector  
detect human faces 
```
rosrun face_detector face_detection_video.py
```

### face_recognizer  
recognize human faces with specific names  
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


### photo_collector  
collect photos of a person for face recognition  
```
rosrun photo_collector img_capture.py
```
