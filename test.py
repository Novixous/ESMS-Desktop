from Detection.emotion_detector import EmotionDetector
from Detection.emotion_stream_handler import EmotionStreamHandler
from Detection.Model.frame_info import FrameInfo
from Detection.Model.session_info import SessionInfo
from Detection.session_evaluator import SessionEvaluator
import cv2
import numpy as np
from path_util import resource_path
import json

# prevents openCL usage and unnecessary logging messages
cv2.ocl.setUseOpenCL(False)

# dictionary which assigns each label an emotion (alphabetical order)
emotion_dict = {7: "No face detected", 0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

cap = cv2.VideoCapture(0)
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# width and height and fps for recording video
width = 426
height = 240
fps = 15

streamHandler = EmotionStreamHandler()
emotionDetector = EmotionDetector()
session_info = SessionInfo(None, None, None, None, None)
video_out = "temp_vid.mp4"
video_writer = cv2.VideoWriter(
            video_out, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
while True:
    hasFace = False
    # Find haar cascade to draw bounding box around face
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    video_writer.write(cv2.resize(frame,(width, height),interpolation = cv2.INTER_CUBIC))
        
    facecasc = cv2.CascadeClassifier(resource_path('Detection\haarcascade_frontalface_default.xml'))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)
    frameInfo = FrameInfo(None, None, None)  

    for (x, y, w, h) in faces:
        hasFace = True
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        maxindex = emotionDetector.detect_emotion(cropped_img)
        cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        streamHandler.add_frame(maxindex)
    if hasFace is not True:
        streamHandler.add_frame(7)
    cv2.imshow('Video', cv2.resize(frame,(1600,960),interpolation = cv2.INTER_CUBIC)) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        session_info = streamHandler.finish()
        video_writer.release()
        with open('data.json', 'w') as outfile:
            json.dump([frame_obj.__dict__ for frame_obj in session_info.frames], outfile)
        break
session_evaluator = SessionEvaluator()
result = session_evaluator.evaluate(session_info)
print("#*#*#*#*# Result:")
print(result)
for i in range(0, len(session_info.periods)):
    print("===={}==== size: {}".format(emotion_dict[i], len(session_info.periods[i])))
    for period in session_info.periods[i]:
        print(period.__dict__)
        duration = int(round((period.period_start - period.period_end)*1000))
cap.release()
cv2.destroyAllWindows() 