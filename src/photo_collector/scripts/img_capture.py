#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# Creating database
# It captures images and stores them in datasets
# folder under the folder name of sub_data
import cv2, sys, numpy, os

haar_file = './src/photo_collector/scripts/haarcascade_frontalface_default.xml'

# All the faces data will be
# present this folder
datasets = './src/face_recognizer/scripts/datasets'

# These are sub data sets of folder,
# for my faces I've used my name you can
# change the label here
# sub_data = 'tianjiao'
sub_data = str(raw_input("Enter name: "))
print(sub_data)

path = os.path.join(datasets, sub_data)
if not os.path.isdir(path):
    os.mkdir(path)

# defining the size of images
(width, height) = (130, 100)

# '0' is used for my webcam,
# if you've any other camera
# attached use '1' like this
face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(0)


def test():
    print("test")


class img_capture():
    def __init__(self):
        rospy.init_node('img_capture', anonymous=True)

        # What we do during shutdown
        rospy.on_shutdown(self.cleanup)

        # Create the cv_bridge object
        self.bridge = CvBridge()

        # Subscribe to the camera image and depth topics and set the appropriate callbacks
        self.image_sub = rospy.Subscriber("/naoqi_driver/camera/front/image_raw", Image, self.image_callback2)

        print("Waiting for image topics...")
        rospy.spin()

    def cleanup(self):
        print
        "Shutting down vision node."
        cv2.destroyAllWindows()

    def image_callback2(self, ros_image):
        # The program loops until it has 30 images of the face.
        count = 1
        while count < 30:
            # Use cv_bridge() to convert the ROS image to OpenCV format
            try:
                im = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
                im = np.array(im, dtype=np.uint8)
            except CvBridgeError, e:
                print
                e

            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (width, height))
                cv2.imwrite('% s/% s.png' % (path, count), face_resize)
            count += 1

            cv2.imshow('OpenCV', im)
            key = cv2.waitKey(10)
            if key == 27:
                break


if __name__ == '__main__':
    test()
    img_capture()
