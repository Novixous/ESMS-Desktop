from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from Detection.EmotionDetector import EmotionDetector
from Detection.EmotionStreamHandler import EmotionStreamHandler
from Detection.Model.FrameInfo import FrameInfo
from Detection.Model.SessionInfo import SessionInfo
import cv2
import numpy as np
import threading
from PathUtil import resource_path
from helpers.observer_helper import ConcreteSubject, ConcreteObserver

# prevents openCL usage and unnecessary logging messages
cv2.ocl.setUseOpenCL(False)

# dictionary which assigns each label an emotion (alphabetical order)
emotion_dict = {7: "No face detected", 0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

class SessionScreen(Widget):
  state = StringProperty("end")
  cap = None
  streamHandler = None
  emotionDetector = None
  sessionInfo = None
  subject = ConcreteSubject()
  kthread = None
  kill = 0

  def startSession(self):
    self.cap = cv2.VideoCapture(0)
    self.streamHandler = EmotionStreamHandler()
    self.emotionDetector = EmotionDetector()
    self.sessionInfo = SessionInfo(None, None, None, None)
    try:
      self.kthread = threading.Thread(target=self.processFrame, args=(self, self.subject), daemon=True)
      self.kthread.start()
      print('-----------------------------------------------------------------')
      print('-----------------------------------------------------------------')
      print('-----------------------------------------------------------------')
      print('-----------------------------------------------------------------')
      self.state = "start"
    except:
      print('Error: unable to start thread')
    while 1:
      pass

  def endSession(self):
    self.kill = 1
    self.subject.send_termination_signal()
    for i in range(0, len(self.sessionInfo.periods)):
      print('===={}==== size: {}'.format(emotion_dict[i], len(self.sessionInfo.periods[i])))
      for period in self.sessionInfo.periods[i]:
        print(period.__dict__)
        duration = int(round((period.periodEnd - period.periodStart)*1000))
    self.cap.release()
    cv2.destroyAllWindows()
    self.state = "end"

  def processFrame(self, _self, subject):
    # def finishProcessing():
    #   subject.detachAll()
    
    # observer = ConcreteObserver(callback=finishProcessing)
    # subject.attach(observer)

    while True:
      hasFace = False
      # Find haar cascade to draw bounding box around face
      ret, frame = _self.cap.read()
      if not ret:
        break
      frame = cv2.flip(frame, 1)

      facecasc = cv2.CascadeClassifier(resource_path('Detection\haarcascade_frontalface_default.xml'))
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)
      frameInfo = FrameInfo(None, None, None)  

      for (x, y, w, h) in faces:
        hasFace = True
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        maxindex = _self.emotionDetector.detectEmotion(cropped_img)
        cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        _self.streamHandler.addFrame(maxindex)
      if hasFace is not True:
        _self.streamHandler.addFrame(7)
      cv2.imshow('ESMS Camera', cv2.resize(frame,(1280,960),interpolation = cv2.INTER_CUBIC))
      if _self.kill == 1:
        _self.sessionInfo = _self.streamHandler.finish()
        break
