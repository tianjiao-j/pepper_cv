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
detect objects (80 classes)  
```
rosrun object_detector yolo_obj_detection.py
```

### photo_collector  
collect photos of a person for face recognition  
```
rosrun photo_collector img_capture.py
```
