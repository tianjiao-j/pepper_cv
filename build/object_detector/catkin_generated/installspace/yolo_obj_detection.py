#!/usr/bin/env python2

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import argparse
import numpy as np


def test():
	print("test")

def get_output_layers(net):
	layer_names = net.getLayerNames()

	output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

	return output_layers

def draw_prediction(classes, COLORS, img, class_id, confidence, x, y, x_plus_w, y_plus_h):
	label = str(classes[class_id])

	color = COLORS[class_id]
	color = tuple(e for e in color)

	# print(class_id, confidence, int(x), y, x_plus_w, y_plus_h, color)
	cv2.rectangle(img, (int(x), int(y)), (int(x_plus_w), int(y_plus_h)), color, 2)

	cv2.putText(img, label, (int(x - 10), int(y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


class object_detector():

	def __init__(self):
		rospy.init_node('yolo_obj_detection', anonymous=True)

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
			image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
			image = np.array(image)
		except CvBridgeError, e:
			print
			e

		Width = image.shape[1]
		Height = image.shape[0]
		scale = 0.00392

		classes = None

		with open('./src/beginner_tutorials/scripts/yolov3.txt', 'r') as f:
			classes = [line.strip() for line in f.readlines()]

		COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
		net = cv2.dnn.readNet('./src/beginner_tutorials/scripts/yolov3.weights', './src/beginner_tutorials/scripts/yolov3.cfg')
		blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
		net.setInput(blob)
		outs = net.forward(get_output_layers(net))

		class_ids = []
		confidences = []
		boxes = []
		conf_threshold = 0.5
		nms_threshold = 0.4

		for out in outs:
			for detection in out:
				scores = detection[5:]
				class_id = np.argmax(scores)
				confidence = scores[class_id]
				if confidence > 0.5:
					center_x = int(detection[0] * Width)
					center_y = int(detection[1] * Height)
					w = int(detection[2] * Width)
					h = int(detection[3] * Height)
					x = center_x - w / 2
					y = center_y - h / 2
					class_ids.append(class_id)
					confidences.append(float(confidence))
					boxes.append([x, y, w, h])

		indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

		for i in indices:
			i = i[0]
		box = boxes[i]
		x = box[0]
		y = box[1]
		w = box[2]
		h = box[3]
		draw_prediction(classes, COLORS, image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))

		cv2.imshow("test", image)

		# Process any keyboard commands
		self.keystroke = cv2.waitKey(5)
		if 32 <= self.keystroke and self.keystroke < 128:
			cc = chr(self.keystroke).lower()
			if cc == 'q':
				# The user has press the q key, so exit
				rospy.signal_shutdown("User hit q key to quit.")

		# Release the VideoCapture object
		#cap.release()

	def cleanup(self):
		print
		"Shutting down vision node."
		cv2.destroyAllWindows()


if __name__ == '__main__':
	test()
	object_detector()
		

