#! /usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class FaceDetector():
    def __init__(self):
        rospy.init_node('face_detection_buche', anonymous=True)

        # What we do during shutdown
        rospy.on_shutdown(self.cleanup)

        # Create the cv_bridge object
        self.bridge = CvBridge()

        # Subscribe to the camera image and depth topics and set the appropriate callbacks
        self.image_sub = rospy.Subscriber("/naoqi_driver/camera/front/image_raw", Image, self.image_callback2)

        print("Waiting for image topics...")
        rospy.spin()

    def image_callback2(self, ros_image):
        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            img = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
        except CvBridgeError, e:
            print e

        # Convert the image to a Numpy array since most cv2 functions
        # require Numpy arrays.
        frame = np.array(img, dtype=np.uint8)
        print(type(frame))

        # Load the cascade
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display
        win_name = "visualization"  #  1. use var to specify window name everywhere
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)  #  2. use 'normal' flag
        cv2.imshow(win_name, img)

        # Process any keyboard commands
        self.keystroke = cv2.waitKey(5)
        if 32 <= self.keystroke and self.keystroke < 128:
            cc = chr(self.keystroke).lower()
            if cc == 'q':
                # The user has press the q key, so exit
                rospy.signal_shutdown("User hit q key to quit.")

    def cleanup(self):
        print "Shutting down vision node."
        cv2.destroyAllWindows()   


if __name__ == '__main__':
        FaceDetector()

