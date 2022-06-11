import cv2
import keras
import numpy as np
from keras.utils import img_to_array
import csv
import time
from datetime import datetime
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

model = keras.models.model_from_json(open("facial_expression_model_structure.json", "r").read())
model.load_weights('facial_expression_model_weights.h5')

emotions = ('angry', 'disgust', 'fear', 'sandhosam', 'Sogam', 'surprise', 'neutral')

x1 =0
y1 =0
z =0

index =0
#web_cam = cv2.VideoCapture(0)
faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

class Video(object):
    def __init__(self):
        self.video=cv2.VideoCapture(1)
        with open('accuracy.csv','a') as f:
            f.truncate(0)
            f.writelines("x,happy,neutral,sad")
            f.writelines('\n')
            f.writelines('1,2,3,4')
            f.writelines('\n')


       
    def __del__(self):
        self.video.release()
    def get_frame(self):
         while self.video.isOpened():
             
            ret, frame = self.video.read()
            frame = cv2.flip(frame, 1)
            faces=faceDetect.detectMultiScale(frame, 1.3, 5)
            for x,y,width,height in faces:
                cv2.rectangle(frame, (x, y), (x+width, y+height), (255, 255, 255), 2)
		
                face = frame[int(y):int(y+height), int(x):int(x+width)]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face = cv2.resize(face, (48, 48))
                
                img = img_to_array(face)
                img = np.expand_dims(img, axis=0)
                img /= 255

                predictions = model.predict(img)
                max_index = np.argmax(predictions[0])
                emotion = emotions[int(max_index)]
                global x1
                global y1
                global z
                if(max_index ==6):
                  
                    
                    
                    if(y1!=5):
                        y1+=1 
                        #y1 = y1 %10
                    if(y1 == 5):
                        y1 = 5
                    
                    x1 =0
                    z =0
                elif(max_index ==3):
                    
                    if(x1!=5):
                        x1 +=1 
                        #x1 = x1 %10
                    else:
                        x1 = 5
                    
                    y1 =0
                    z =0
                elif(max_index == 4):
                    
                    #z = z %10
                    if(z !=5):
                        z += 1
                        #z = z %10
                    else:
                        z = 5
                    x1 =0
                    y1 =0
                global index 
                
                    
                with open('accuracy.csv','a') as file :
                    index+=1
                    
                    file.writelines(str(index) +',' +str(x1) +',' +str(y1)+','+ str(z))
                    
                    file.writelines('\n')
                    print(max_index)

                now = datetime.now()
                mytime = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + ":" + str(now.microsecond)
                
                with open ("ak.txt",'a')as file:

                #time.sleep(1)
                    file.write(emotion)
                    file.write("\t")
                    file.writelines(mytime)
                    file.write("\n")
                
                    
                


               

       

                cv2.putText(frame, emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            #cv2.imshow('Real time facial expression', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            ret,jpg=cv2.imencode('.jpg',frame)
            return jpg.tobytes()
    
