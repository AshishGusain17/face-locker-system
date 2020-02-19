import face_recognition
import cv2,os
import numpy as np
import imutils,time
from imutils.video import VideoStream


print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
def fun(name):
	ct=0
	print("Loading face detector...")
	protoPath = os.path.sep.join(['caffe_model', "deploy.prototxt"])
	modelPath = os.path.sep.join(['caffe_model', "res10_300x300_ssd_iter_140000.caffemodel"])
	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)




	vs = VideoStream(src=0).start()
	time.sleep(2.0)
	while 1:
		frame = vs.read()

		# print(ct,frame.shape)
		frame = imutils.resize(frame, width=600)
		h,w = frame.shape[:2]


		imageBlob = cv2.dnn.blobFromImage(frame, 1.0, ((300,300)),(0,0,0), swapRB=False, crop=False)
		detector.setInput(imageBlob)
		detections = detector.forward()
		less=0
		for i in range(0, detections.shape[2]): 
			confidence = detections[0, 0, i, 2]
			if confidence > less:
				box = detections[0, 0, i, 3:7] * np.array([w,h,w,h])
				(startX, startY, endX, endY) = box.astype("int")
				less=confidence
		# print(startX, startY, endX, endY)
		print(less)

		cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
	
		if ct>=50 and less>=0.9:
			newimg=frame[startY: endY, startX: endX]
			newimg = cv2.cvtColor(newimg, cv2.COLOR_BGR2RGB)
			print(newimg.shape)
			cv2.imwrite("static/images/"+name + ".jpg",newimg)
			break
		cv2.imshow('face',frame)
		key = cv2.waitKey(1) & 0xFF

		if key == ord("q"):
			break
		ct=ct+1


	cv2.destroyAllWindows()
	vs.stop()