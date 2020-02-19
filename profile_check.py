import face_recognition
import cv2,os
import numpy as np
import imutils,time
from imutils.video import VideoStream

def pic_confirm(name):
	print("Loading face detector...")
	protoPath = os.path.sep.join(['caffe_model', "deploy.prototxt"])
	modelPath = os.path.sep.join(['caffe_model', "res10_300x300_ssd_iter_140000.caffemodel"])
	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)


	img1 = face_recognition.load_image_file("static/images/"+name + ".jpg")
	e1=face_recognition.face_encodings(img1)[0]


	print("Starting video stream...")
	# vs = cv2.VideoCapture(0)
	vs = VideoStream(src=0).start()

	time.sleep(2.0)
	ct=0
	ret = False
	predt,predf=0,0
	while True:
		# _,frame = vs.read()
		frame=vs.read()
		frame = imutils.resize(frame, width=600)
		h,w = frame.shape[:2]

		imageBlob = cv2.dnn.blobFromImage(frame, 1.0, ((300,300)),(0,0,0), swapRB=False, crop=False)
		detector.setInput(imageBlob)
		detections = detector.forward()
		less=0

		for i in range(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]
			if confidence > less:
				box = detections[0, 0, i, 3:7] * np.array([600, 449,600,449])
				(startX, startY, endX, endY) = box.astype("int")
				less=confidence
		print(less,len(detections))

		if ct>=30 and less>0.8:
			cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
			newframe=frame[startY:endY,startX:endX]

			if predt>=5 :
				ret=True
				break
			if predf>=30:
				ret=False
				break
			try:
				e2=face_recognition.face_encodings(newframe)[0]
				ret=face_recognition.compare_faces([e1],e2)
				if ret==False:
					predf=predf+1
					print("false cases = ",predf)
				else:
					predt=predt+1
					print("true cases = ",predt)
			except:
				pass

				
		ct=ct+1
		cv2.imshow("Profile-check", frame)

		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

	cv2.destroyAllWindows()
	vs.stop()
	return ret


