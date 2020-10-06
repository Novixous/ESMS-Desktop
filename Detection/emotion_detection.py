import numpy as np
import cv2
import time
from datetime import datetime
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from Model.FrameInfo import FrameInfo
from Model.SessionInfo import SessionInfo
from Model.PeriodInfo import PeriodInfo

model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

model.load_weights('model-epoch-30.h5')

# prevents openCL usage and unnecessary logging messages
cv2.ocl.setUseOpenCL(False)

# dictionary which assigns each label an emotion (alphabetical order)
emotion_dict = {7: "No face detected", 0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# duration in miliseconds to be considered a valid emotion period
emotion_valid_duration = {7: 300,0: 300, 1: 300, 2: 300, 3: 300, 4: 300, 5: 300, 6: 300}
emotion_maximum_buffer_duration = {7: 300, 0: 300, 1: 300, 2: 300, 3: 300, 4: 300, 5: 300, 6: 300}

# period_group = {7: "No face detected", 0: "Neutral", 1: "Positive", 2: "Negative"}
# emotion_group_dict = {0: 2, 1: 2, 2: 2, 3: 1, 4: 0, 5: 2, 6: 1}

# start the webcam feed
def startCamera():
    
    frames = []
    currentFrame = FrameInfo(None, None, None)
    previousFrame = FrameInfo(None, None, None)
    periods = []
    tempDurations = []
    for i in range (0, 8):
        periods.append([])
        tempDurations.append([0,0])
    beginSession = 0
    tempTime = 0

    cap = cv2.VideoCapture(0)
    while True:
        hasFace = False
        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        if beginSession == 0:
            beginSession = time.time()
            tempTime = time.time()
        else:
            tempTime = time.time()
        passedTime = int(round((tempTime - beginSession)*1000))
        facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)    

        for (x, y, w, h) in faces:
            hasFace = True
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img)            
            maxindex = int(np.argmax(prediction))
            currentFrame = FrameInfo(tempTime, passedTime, maxindex)
            frames.append(currentFrame)
            cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        if hasFace is not True:
            currentFrame = FrameInfo(tempTime, passedTime, 7)
            frames.append(currentFrame)      
        if  len(frames) >= 2:
            previousFrame = frames[len(frames)-2]
            for i in range(0, 8):
                duration = int(round((currentFrame.timeStamp - previousFrame.timeStamp)*1000))
                if previousFrame.emotion == i and tempDurations[i] == [0,0]:
                    periods[i].append(PeriodInfo(previousFrame.timeStamp, currentFrame.timeStamp, i))
                    tempDurations[i][0] += duration
                elif previousFrame.emotion == i and tempDurations[i] != [0,0]:
                    tempDurations[i][0] += duration
                    periods[i][len(periods[i])-1].periodEnd = currentFrame.timeStamp
                    periods[i][len(periods[i])-1].update()
                    tempDurations[i][1] = 0
                elif previousFrame.emotion != i and tempDurations[i] == [0,0]:
                    pass
                elif previousFrame.emotion != i and tempDurations[i] != [0,0]:
                    if tempDurations[i][0] >= emotion_valid_duration[i]:
                        tempDurations[i][1] += duration
                        if tempDurations[i][1] >= emotion_maximum_buffer_duration[i]:
                            tempDurations[i] = [0,0]
                    else:                        
                        tempDurations[i] = [0,0]
                        duration = int(round((periods[i][len(periods[i])-1].periodEnd - periods[i][len(periods[i])-1].periodStart)*1000))
                        del(periods[i][len(periods[i])-1])

        
        cv2.imshow('Video', cv2.resize(frame,(1600,960),interpolation = cv2.INTER_CUBIC))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # ****** print out all periods ******
            for i in range(0, len(periods)):
                print("===={}==== size: {}".format(emotion_dict[i], len(periods[i])))
                for period in periods[i]:
                    print(period.__dict__)
                    duration = int(round((period.periodEnd - period.periodStart)*1000))
            print("__________________________________________________________________________________________")
            print("__________________________________________________________________________________________")
            break

    sessionInfo = SessionInfo(frames, beginSession, tempTime, periods)  
    cap.release()
    cv2.destroyAllWindows()
    return sessionInfo

sessionInfo = startCamera()

# for faceFrame in sessionInfo.frames:
#     print(faceFrame.__dict__)
# print("beginSession: {}", sessionInfo.sessionBeggin)
# print("endSession: {}", sessionInfo.sessionEnd)