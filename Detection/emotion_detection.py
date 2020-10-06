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
from Model.SectionInfo import SectionInfo

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

# duration in miliseconds to be considered a valid emotion section
emotion_valid_duration = {7: 5000,0: 300, 1: 300, 2: 300, 3: 600, 4: 800, 5: 300, 6: 300}
emotion_maximum_buffer_duration = {7: 300, 0: 300, 1: 300, 2: 300, 3: 300, 4: 300, 5: 300, 6: 300}

section_group = {7: "No face detected", 0: "Neutral", 1: "Positive", 2: "Negative"}
emotion_group_dict = {0: 2, 1: 2, 2: 2, 3: 1, 4: 0, 5: 2, 6: 1}

# start the webcam feed
def startCamera():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frames = []
    currentFrame = FrameInfo(None, None, None)
    previousFrame = FrameInfo(None, None, None)
    tempSection = SectionInfo(None, None, None)
    sections = []
    tempDurations = []
    for i in range (0, 7):
        sections.append([])
        tempDurations.append([0,0])
    beginSession = 0
    tempTime = 0
    frameCount = 0
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
            # cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
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
            for i in range(0, 7):
                if previousFrame.emotion == i and tempDurations[i] == [0,0]:
                    sections[i].append(SectionInfo(previousFrame.timeStamp, previousFrame.timeStamp))

        cv2.imshow('Video', cv2.resize(frame,(1600,960),interpolation = cv2.INTER_CUBIC))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(len(sections[4]))
            break

    sessionInfo = SessionInfo(frames, beginSession, tempTime)  
    cap.release()
    cv2.destroyAllWindows()
    return sessionInfo

# def mergeFramesToSections(sessionInfo):
#     sections = []
#     for x in range(0, len(sessionInfo.frames)):
#         currentFrame = sessionInfo.frames[x]
#         if x == 0:
#             sections.append(SectionInfo(sessionInfo.sessionBeggin, currentFrame.timeStamp, currentFrame.emotion))
#         else:
#             if currentSection.status == currentFrame.emotion:
#                 currentSection.sectionEnd = currentFrame.timeStamp
#             else:
#                 currentSection.sectionEnd = currentFrame.timeStamp
#                 sections.append(SectionInfo(currentFrame.timeStamp, currentFrame.timeStamp, currentFrame.emotion))

#         # elif x == len(sessionInfo.frames)-1:
#         #     if currentFrame.emotion == currentSection.status:
#         #         currentSection.sectionEnd = currentFrame.timeStamp
#         #     else:
#         #         sections.append(SectionInfo(previousFrame.timeStamp, currentFrame.timeStamp, currentFrame.emotion))
#         #     if (sessionInfo.sessionEnd - currentFrame.timeStamp) > 0:
#         #         sections.append(SectionInfo(currentFrame.timeStamp, sessionInfo.sessionEnd, -1))
#         # else:
#         #     duration = int(round((currentFrame.timeStamp - previousFrame.timeStamp)*1000))
#         #     if duration > 10000:
#         #         if currentSection.status == -1:
#         #             currentSection.sectionEnd = currentFrame.timeStamp
#         #         else:
#         #             sections.append(SectionInfo(previousFrame.timeStamp, currentFrame.timeStamp, -1))
#         #     else:
#         #         if currentFrame.emotion == currentSection.status:
#         #             currentSection.sectionEnd = currentFrame.timeStamp
#         #         else:
#         #             currentSection.sectionEnd = currentFrame.timeStamp
#         #             sections.append(SectionInfo(previousFrame.timeStamp, currentFrame.timeStamp, currentFrame.emotion))
#     return sections

# def filterNoise(sections):
#     for x in range(0, len(sections)-1):
#         if (x == 0 and sections[x].status != -1) or (x > 0):
#             for y in range(x, len(sections)-1):
#                 print("+1")
#     return sections

# def mergeSections(sections):
#     for x in reversed(range(len(sections))):
#         if sections[x-1].status == sections[x].status:
#             sections[x-1].sectionEnd = sections[x].sectionEnd
#             del sections[x]
#     return sections

# def printSessionInfo(sessionInfo):
#     print("Sections count: {}", len(sessionInfo.sections))
#     print(datetime.fromtimestamp(sessionInfo.sessionBeggin))
#     print("=======================================================")
#     for section in sessionInfo.sections:
#         print(emotion_dict[section.status])
#         print(datetime.fromtimestamp(section.sectionStart))
#         print(datetime.fromtimestamp(section.sectionEnd))
#         print("duration: {}", int(round((section.sectionEnd-section.sectionStart)*1000)))
#         print("=======================================================")    
#     print(datetime.fromtimestamp(sessionInfo.sessionEnd))

sessionInfo = startCamera()
# sections = mergeFramesToSections(sessionInfo)
# sections = filterNoise(sections)
# # sections = mergeSections(sections)
# sessionInfo.sections = sections
# printSessionInfo(sessionInfo)
print("beginSession: {}", sessionInfo.sessionBeggin)
print("endSession: {}", sessionInfo.sessionEnd)
for faceFrame in sessionInfo.frames:
    print(faceFrame.__dict__)
