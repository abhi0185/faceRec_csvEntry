import face_recognition
import cv2
import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from sklearn.neighbors import KNeighborsClassifier
import time
import multiprocessing
from  multiprocessing import Process, Queue
import itertools
#from Queue import Queue
#import concurrent.futures
#import random

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def capture(q):
    video_capture = cv2.VideoCapture("rtsp://admin:q12345678@192.168.7.9:554/Streaming/Channels/101 RTSP/1.0")
    process_this_frame = 0
    i=0
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = frame	#cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = small_frame

        if process_this_frame == 30:
            q.put(rgb_small_frame)
            i = i + 1
            print("got frame : ",i)
            print("queue length : ", q.qsize())
            process_this_frame = 1
        process_this_frame = process_this_frame + 1
     

#def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.5):
def predict(img_queue, knn_clf=None, model_path=None, distance_threshold=0.5):
    #    print "arguments", arguments
    #    print "x img path", X_img_path
    #    print "knn clf", knn_clf
        
    #if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
    #    raise Exception("Invalid image path: {}".format(X_img_path))

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        t = time.time()
        print('reading start')
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)
        print("time taken in reading file ",time.time()-t)

    while True:
        currentframe = []
        
        X_img_path = img_queue.get()
        # Load image file and find face locations
        currentframe.append(X_img_path)
        t1 = time.time()
        #X_face_locations = face_recognition.face_locations(X_img)	#,model="cnn")
        batch_of_face_locations = face_recognition.batch_face_locations(currentframe, number_of_times_to_upsample=0)
        print("time taken in face location ",time.time()-t1)
        for frame_number_in_batch, X_face_locations in enumerate(batch_of_face_locations):
            print('live face location : ',X_face_locations)

            # If no faces are found in the image, return an empty result.
            if len(X_face_locations) == 0:
                #return []
                print('')
            else:
                
                t2 = time.time()
                # Find encodings for faces in the test iamge
                faces_encodings = face_recognition.face_encodings(X_img_path, known_face_locations=X_face_locations)
                print("total time taken in face encoding ",time.time()-t2)
                # Use the KNN model to find the best matches for the test face

                
                t3 = time.time()
                closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
                are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
                print("total time taken in matching ",time.time()-t3)
                
                t4 = time.time()
                haha = [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]
                
                for name, (top, right, bottom, left) in haha:
                    print(name)
                print("total time taken in guessing name ",time.time()-t4)
            


    # Predict classes and remove classifications that aren't within the threshold

'''
'''   

i = 0   
    

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = 0
#print("Training KNN classifier...")
#classifier = train("images", model_save_path="trained_knn_model.clf", n_neighbors=2)
#print("Training complete!")

predictions = []

q = Queue()
p1 = Process(target=capture, args=(q,))
p1.start()
#time.sleep(1)
#p2 = Process(target=predict, args=(q, None, "trained_knn_model.clf"))
#p2.start()
#time.sleep(1)
#p3 = Process(target=predict, args=(q, None, "trained_knn_model.clf"))
#p3.start()

print('reading start')
with open("trained_knn_model.clf", 'rb') as f:
    knn_clf = pickle.load(f)

predict(q, knn_clf)
    

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

