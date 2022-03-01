#!/usr/bin/env python
# license removed for brevity
import rospy

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String
import cv2


def test():
    print("test")


class face_detection_video():
    def __init__(self):
        rospy.init_node('face_detection_video', anonymous=True)

        # What we do during shutdown
        rospy.on_shutdown(self.cleanup)

        # Create the cv_bridge object
        self.bridge = CvBridge()

        # Subscribe to the camera image and depth topics and set the appropriate callbacks
        self.image_sub = rospy.Subscriber("/naoqi_driver/camera/front/image_raw", Image, self.image_callback2)

        print("Waiting for image topics...")
        rospy.spin()

    def image_callback2(self, ros_image):
        # Load the cascade
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # To capture video from webcam.
        # cap = cv2.VideoCapture(0)
        # To use a video file as input
        # cap = cv2.VideoCapture('filename.mp4')

        while True:
            # Use cv_bridge() to convert the ROS image to OpenCV format
            try:
                img = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
            except CvBridgeError, e:
                print e
            # Read the frame
            # _, img = cap.read()
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect the faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            # Draw the rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # Display
            cv2.imshow('img', img)
            # Stop if escape key is pressed
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        # Release the VideoCapture object
        # cap.release()

    def cleanup(self):
        print "Shutting down vision node."
        cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        test()
        face_detection_video()
    except rospy.ROSInterruptException:
        pass
