from Detection.EmotionDetector import EmotionDetector
from Detection.EmotionStreamHandler import EmotionStreamHandler
from Detection.Model.FrameInfo import FrameInfo
from Detection.Model.SessionInfo import SessionInfo
import cv2
import numpy as np

# prevents openCL usage and unnecessary logging messages
cv2.ocl.setUseOpenCL(False)

# dictionary which assigns each label an emotion (alphabetical order)
emotion_dict = {7: "No face detected", 0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

cap = cv2.VideoCapture(0)
streamHandler = EmotionStreamHandler()
emotionDetector = EmotionDetector()
sessionInfo = SessionInfo(None, None, None, None)
while True:
    hasFace = False
    # Find haar cascade to draw bounding box around face
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    facecasc = cv2.CascadeClassifier('Detection\haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)
    frameInfo = FrameInfo(None, None, None)  

    for (x, y, w, h) in faces:
        hasFace = True
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        maxindex = emotionDetector.detectEmotion(cropped_img)
        cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        frameInfo.emotion = maxindex
    if hasFace is not True:
        frameInfo.emotion = 7
    streamHandler.addFrame(frameInfo)
    cv2.imshow('Video', cv2.resize(frame,(1600,960),interpolation = cv2.INTER_CUBIC)) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        sessionInfo = streamHandler.finish()
        break
for i in range(0, len(sessionInfo.periods)):
    print("===={}==== size: {}".format(emotion_dict[i], len(sessionInfo.periods[i])))
    for period in sessionInfo.periods[i]:
        print(period.__dict__)
        duration = int(round((period.periodEnd - period.periodStart)*1000))
cap.release()
cv2.destroyAllWindows() 