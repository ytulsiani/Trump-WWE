import cv2
import cv2 as cv
import numpy as np
import os

trumpVideo = './vid1.mp4'
overlay = './overlay.jpg'
cap = cv2.VideoCapture(trumpVideo)
img = cv2.imread(trumpVideo)
vidcap = cv2.VideoCapture('./vid1.mp4')
success,image = vidcap.read()
count = 0
success = True
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
while success:
  success,image = vidcap.read()
  print 'Read a new frame: ', success
  cv2.imwrite(dir_path + "/frames/" + "frame%d.jpg" % count, image)     # save frame as JPEG file
  count += 1

total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.m4v', fourcc, 1, (640, 360))
frame = cv2.imread('./frame242.jpg')
out.write(frame)

for i in range(total):
    break
out.release()
cap.release()
