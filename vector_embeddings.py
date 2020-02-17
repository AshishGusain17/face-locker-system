# python vector_embeddings.py -i image_dataset -e output/vector_embeddings.pickle -d caffe_model -m openface_nn4.small2.v1.t7

from imutils import paths
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset",         required=True,help="path to input directory of faces + images")
ap.add_argument("-e", "--embeddings",      required=True,help="path to output serialized db of facial embeddings")
ap.add_argument("-d", "--detector",        required=True,help="path to OpenCV's deep learning face detector")
ap.add_argument("-m", "--embedding-model", required=True,help="path to OpenCV's deep learning face embedding model")
ap.add_argument("-c", "--confidence",      type=float, default=0.5,help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load our serialized face detector from disk
print("Loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"], "res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# load our serialized face embedding model from disk
print("Loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])

# grab the paths to the input images in our dataset
print("Get each image from all folders in the dataset")
imagePaths = list(paths.list_images(args["dataset"]))
print(imagePaths)

# knownEmbeddings to store vector_embeddings
# knownNames to store names of people whose faces are to be detected
knownEmbeddings = []
knownNames = []

total = 0
for (i, imagePath) in enumerate(imagePaths):
	print("Processing image {}/{}".format(i + 1,len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	image = cv2.imread(imagePath)
	image = imutils.resize(image, width=600)
	(h, w) = image.shape[:2]

	# construct a blob from the image
	imageBlob = cv2.dnn.blobFromImage(
		cv2.resize(image, (300, 300)), 1.0, (300, 300),
		(104.0, 177.0, 123.0), swapRB=False, crop=False)

	# detect the location of faces
	detector.setInput(imageBlob)
	detections = detector.forward()
	print(detections.shape)

	if len(detections) > 0:
		# each training image should have only 1 face, so the prediction box with maximum probablity is selected
		i = np.argmax(detections[0, 0, :, 2])
		confidence = detections[0, 0, i, 2]
		
		# to ensure that the face detected has enough confidence
		if confidence > args["confidence"]:

			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# extract the face ROI and grab the ROI dimensions
			face = image[startY:endY, startX:endX]
			(fH, fW) = face.shape[:2]

			# ensure that the face is sufficient to be vector_embedded
			if fW < 20 or fH < 20:
				continue

			# construct a blob for the face ROI
			faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
			embedder.setInput(faceBlob)
			vec = embedder.forward()
			print(vec.shape)
			
			knownNames.append(name)
			knownEmbeddings.append(vec.flatten())
			print(vec.flatten().shape)
			total += 1

# dump the facial embeddings + names to disk
print("vector_embedded {} images into the pickle file".format(total))
data = {"embeddings": knownEmbeddings, "names": knownNames}
f = open(args["embeddings"], "wb")
f.write(pickle.dumps(data))
f.close()



# 0 1    90%

#0 0    upgood/downwrong



# 1 1 best

# 1 0 good/wrong

