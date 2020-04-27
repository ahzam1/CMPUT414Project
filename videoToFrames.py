import cv2
import imutils
import numpy as np
from math import cos, sin, radians
# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# To capture video from webcam. 
cap = cv2.VideoCapture(0)
# To use a video file as input 
#cap = cv2.VideoCapture('test.mp4')


### TAKEN FROM https://stackoverflow.com/questions/5015124/rotated-face-detection, USED FOR ROTATING IMAGES BACK AND FORTH.
def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]
###  



while True:
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale  
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    # if isinstance(faces,tuple):
    #     #try rotating and attempting to find face here.
    #     rotl = rotate_image(img, -45)
    #     rotr = rotate_image(img, 45)
    #     grayR = cv2.cvtColor(rotr, cv2.COLOR_BGR2GRAY)
    #     grayL = cv2.cvtColor(rotl, cv2.COLOR_BGR2GRAY)
    #     facesr = face_cascade.detectMultiScale(grayR, 1.3, 4)
    #     facesl = face_cascade.detectMultiScale(grayL, 1.3, 4)
   
    finalFaces = []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        finalFaces.append(img[y:y+h, x:x+w])
    # if 'facesl' in locals():
    #     for a in facesl:
    #         a = [rotate_point(a, img, -45)]
    #     for (x, y, w, h) in facesl:
    #         cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    #         finalFaces.append(img[y:y+h, x:x+w])
    #     del facesl
    # if 'facesr' in locals():
    #     for a in facesr:
    #         a = [rotate_point(a, img, 45)]
    #     for (x, y, w, h) in facesr:
    #         cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    #         finalFaces.append(img[y:y+h, x:x+w])
    #     del facesr # to ensure it doesn't store old ones.
    for face in finalFaces:
        # face within face, if any found
        grayf =cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        avg_color_per_row = np.average(grayf, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        for i in range(len(avg_color_per_row)):
            if abs(avg_color-avg_color_per_row[i])<10:
                cv2.line(face, (0, i), (grayf.shape[1], i), (0,255,0), 2)
                searchBelow = i
                break
        roi_gray = grayf[i:-1,:]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        #for (ex,ey,ew,eh) in eyes: 
            #cv2.rectangle(face,(ex,ey),(ex+ew,ey+eh),(0,127,255),2)
    cv2.imshow('img',img)
    # cv2.imshow('img', img)
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

# Release the VideoCapture object
cap.release()

