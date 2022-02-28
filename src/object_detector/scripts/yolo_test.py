#! /usr/bin/env python

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


def detect_object():
		#image = cv2.imread(args.image)

		# To capture video from webcam.
		cap = cv2.VideoCapture(0)
		# To use a video file as input
		# cap = cv2.VideoCapture('filename.mp4')

		while True:
			# Read the frame
			_, image = cap.read()
			#print(type(image))
			Width = image.shape[1]
			Height = image.shape[0]
			scale = 0.00392

			classes = None

			face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
			with open('yolov3.txt', 'r') as f:
				classes = [line.strip() for line in f.readlines()]

			COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
			net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
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
			# Stop if escape key is pressed
			k = cv2.waitKey(30) & 0xff
			if k == 27:   #ESC
				break

		# Release the VideoCapture object
		cap.release()

if __name__ == '__main__':
	test()
	detect_object()
		
