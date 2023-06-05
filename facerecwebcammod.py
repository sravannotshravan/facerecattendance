#Importing all necessary modules
import cv2
import simple_facerecmod as sfr
import statistics as s
import os
#Encode faces from the folder
#def MakeDir():
#    if not os.path.exists('D:\FaceRecAttendanceFaces'):
#        os.mkdir('D:\FaceRecAttendanceFaces')
#        print("Made dir")
def LoadFaces():
    sfr.load_encoding_images('Faces/')
    return sfr.knownfaces()

#Loading webcam



def FaceRecDemo():
    LoadFaces()
    samplespace=[]
    cap=cv2.VideoCapture(0)
    ukc=0
    while True:
        ret,frame=cap.read()
        #Detect faces
        face_locations,face_names=sfr.detect_known_faces(frame)
        for face_loc,name in zip(face_locations, face_names):
            y1,x1,y2,x2=tuple(face_loc)
            cv2.rectangle(frame, (x1,y1),(x2,y2),(0,200,0),4)
            cv2.putText(frame,name,(x2,y2+20),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
            print(name)
            cv2.imshow("Frame", frame)
            key=cv2.waitKey(1)
'''            samplespace.append(name)
            if name=="Unknown":
                ukc+=1

        if ukc >= 10:
            print("This face is not identified. If this face is added in the database, please try a few things such as cleaning the camera or removing any covering on the face.")
            break
        if len(samplespace)==20:
            break
    cap.release()
    cv2.destroyAllWindows()
    print("The face is identified as ",s.mode(samplespace))'''

def FaceRec(samples=20):
    samplespace=[]
    cap=cv2.VideoCapture(0)
    while True:
        ret,frame=cap.read()
        #Detect faces
        face_locations,face_names=sfr.detect_known_faces(frame)
        for face_loc,name in zip(face_locations, face_names):
            y1,x1,y2,x2=tuple(face_loc)
            cv2.rectangle(frame, (x1,y1),(x2,y2),(0,200,0),4)
            cv2.putText(frame,name,(x2,y2+20),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
            print(name)
            samplespace.append(name)
        cv2.imshow("Frame", frame)
        key=cv2.waitKey(1)
        if len(samplespace)>=samples:
            break
    cap.release()
    cv2.destroyAllWindows()
    return(s.mode(samplespace))
#MakeDir()
#LoadFaces()
#print("Face is",FaceRec(20))
