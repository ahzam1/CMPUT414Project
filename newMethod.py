import cv2
from imutils import face_utils
import imutils
import dlib
import numpy as np
from math import cos, sin, radians

# To capture video from webcam. 
cap = cv2.VideoCapture(0)
# To use a video file as input 
#cap = cv2.VideoCapture('test.mp4')

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

####
# 0-16 is the jawline
# 17-21 is right eyebrow
# 22-26 is left eyebrow
# 27-30 is nose bridge
# 31-35 is the nose bottom
# 36-41 is right eye
# 42-47 is left eye
# 48-59 is outer lip trace
# 60-67 is inner lip trace
####
f = open("extractions.txt", "w")

count =0 
while True:
	f.write("\nframe:" + str(count))
	count +=1
    # Read the frame
	_, img = cap.read()
	#set a fixed size
	# image = imutils.resize(img, width=500)
	#grayscale convert
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#use dlib face detector
	rects = detector(gray, 0)
    # loop over the face detections
	for (i, rect) in enumerate(rects):
		# abstracted from https://www.pyimagesearch.com/2017/04/10/detect-eyes-nose-lips-jaw-dlib-opencv-python/
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)
		drawn = img.copy()
		# loop over the face parts individually
		for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
			# clone the original image, iterate over landmarks, and draw dots on their x,y position
			for (x, y) in shape[i:j]:
				cv2.circle(drawn, (x, y), 2, (0, 0, 255), -1)

		# show the drawn on image
		cv2.imshow("Image", drawn)
		f.write(np.array2string(shape))

    # Stop if escape key is pressed
	k = cv2.waitKey(30) & 0xff
	if k==27:
		break

# Release the VideoCapture object
cap.release()
f.close()

