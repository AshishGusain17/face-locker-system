# python train.py -e output/vector_embeddings.pickle -r output/recognizer.pickle -l output/encoder.pickle

from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle

ap = argparse.ArgumentParser()
ap.add_argument("-e", "--embeddings", required=True,help="path to serialized db of facial embeddings")
ap.add_argument("-r", "--recognizer", required=True,help="path to output model trained to recognize faces")
ap.add_argument("-l", "--encoder",         required=True,help="path to output label encoder")
args = vars(ap.parse_args())

# load the face vector_embeddings
print("Loading face embeddings from other file...")
data = pickle.loads(open(args["embeddings"], "rb").read())
print(len(data))
# encode the labels
print("Encoding of the labels...")
encoder = LabelEncoder()
labels = encoder.fit_transform(data["names"])
print(encoder)
print(labels)
# train the model used to accept the 128-d embeddings of the face and
# then produce the actual face recognition
print("Training of the model...")
recognizer = SVC(C=1.0, kernel="poly", probability=True)
recognizer.fit(data["embeddings"], labels)
print(recognizer)
# write the actual face recognition model to disk
f = open(args["recognizer"], "wb")
f.write(pickle.dumps(recognizer))
f.close()

# write the label encoder to disk
f = open(args["encoder"], "wb")
f.write(pickle.dumps(encoder))
f.close()