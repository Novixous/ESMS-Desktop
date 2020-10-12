from core.kbutton import KMDRectangleFlatButton
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import cv2
import numpy as np
import threading
import socket
from Detection.EmotionDetector import EmotionDetector
from Detection.EmotionStreamHandler import EmotionStreamHandler
from Detection.Model.FrameInfo import FrameInfo
from Detection.Model.SessionInfo import SessionInfo
from Detection.SessionEvaluator import SessionEvaluator
from PathUtil import resource_path
from helpers.ksocket import KSocketClient

class SessionButton(KMDRectangleFlatButton):
  stream_port = 9090
  term_port = 9091
  image_source = ObjectProperty()
  status = 'ended'

  def action(self, *args):
    if self.status == 'ended':
      self.status = 'started'
      new_thread = threading.Thread(target=self.detect_from_camera, daemon=True)
      new_thread.start()
      Clock.schedule_interval(self.client_recv, 0.1)
      self.ids.lbl_txt.text = 'End SESSION'
    else:
      self.status = 'ended'
      self.ids.lbl_txt.text = 'Start SESSION'


  def client_recv(self, *args):
    self.client_stream_socket = KSocketClient()
    self.client_stream_socket.kconnect(socket.gethostname(), self.stream_port)
    str_encoded = self.client_stream_socket.kreceive()
    nparr = np.fromstring(str_encoded, np.uint8)
    if nparr.size != 0:
      img_decoded = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
      # try:
      if self.status == 'started':
        cv2.imwrite(resource_path('assets/video/video.jpg'), img_decoded)
        self.image_source.source = 'assets/video/video.jpg'
        self.image_source.reload()
      else:
        self.image_source.source = 'assets/video.jpg'
        self.image_source.reload()
      # except:
      #   pass

  def detect_from_camera(self):
    # try:
    server_stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_stream_socket.bind((socket.gethostname(), self.stream_port))
    server_stream_socket.listen()
    print(f'\nServer started at {str(socket.gethostbyname(socket.gethostname()))} at port {str(self.stream_port)}')
    # prevents openCL usage and unnecessary logging messages
    cv2.ocl.setUseOpenCL(False)

    # dictionary which assigns each label an emotion (alphabetical order)
    emotion_dict = {7: "No face detected", 0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    cap = cv2.VideoCapture(0)
    streamHandler = EmotionStreamHandler()
    emotionDetector = EmotionDetector()
    sessionInfo = SessionInfo(None, None, None, None)

    while True:
      (connection, address) = server_stream_socket.accept()
      hasFace = False
      # Find haar cascade to draw bounding box around face
      ret, frame = cap.read()
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
        maxindex = emotionDetector.detectEmotion(cropped_img)
        cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        streamHandler.addFrame(maxindex)
      if hasFace is not True:
        streamHandler.addFrame(7)
      img = cv2.resize(frame,(1280,960),interpolation = cv2.INTER_CUBIC)
      img_encoded = cv2.imencode('.jpg', img)[1]
      data_encoded = np.array(img_encoded)
      str_encoded = data_encoded.tostring()
      connection.sendall(str_encoded)
      connection.close()
      if self.status == 'ended':
        sessionInfo = streamHandler.finish()
        Clock.unschedule(self.client_recv)
        break
      else:
        continue
    for i in range(0, len(sessionInfo.periods)):
      print("===={}==== size: {}".format(emotion_dict[i], len(sessionInfo.periods[i])))
      for period in sessionInfo.periods[i]:
        print(period.__dict__)
        duration = int(round((period.periodEnd - period.periodStart)*1000))
    sessionEvaluator = SessionEvaluator()
    sessionEvaluator.evaluate(sessionInfo)
    cap.release()
    cv2.destroyAllWindows() 
    # except:
    #   pass
