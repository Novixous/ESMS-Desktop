import cv2
import numpy as np
import threading
import socket
import os
from Detection.emotion_detector import EmotionDetector
from Detection.emotion_stream_handler import EmotionStreamHandler
from Detection.Model.frame_info import FrameInfo
from Detection.Model.session_info import SessionInfo
from Detection.session_evaluator import SessionEvaluator
from path_util import resource_path

class TestSocket():

  def __init__(self):
    self.stream_port = 9090

  def detect_from_camera(self):
    # try:
    print('Try to create socket')
    server_stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_stream_socket.bind((socket.gethostname(), self.stream_port))
    server_stream_socket.listen()
    print('Socket created')
    # prevents openCL usage and unnecessary logging messages
    cv2.ocl.setUseOpenCL(False)

    # dictionary which assigns each label an emotion (alphabetical order)
    emotion_dict = {7: 'No face detected', 0: 'Angry', 1: 'Disgusted', 2: 'Fearful', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprised'}
    # emotion_colors = {7: '#000000', 0: '#FF005A', 1: '#33CC33', 2: '#9933FF', 3: '#FFCC00', 4: '#996600', 5: '#0099FF', 6: '#33CCCC'}

    cap = cv2.VideoCapture(0)
    streamHandler = EmotionStreamHandler()
    emotionDetector = EmotionDetector()
    sessionInfo = SessionInfo(None, None, None, None, None)

    while True:
      print('Waiting for connection')
      (connection, address) = server_stream_socket.accept()
      hasFace = False
      # Find haar cascade to draw bounding box around face
      print('Get image from camera')
      ret, frame = cap.read()
      print('Get success')
      if not ret:
        break
      frame = cv2.flip(frame, 1)

      facecasc = cv2.CascadeClassifier(resource_path('Detection\haarcascade_frontalface_default.xml'))
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)
      frameInfo = FrameInfo(None, None, None)

      for (x, y, w, h) in faces:
        hasFace = True
        roi_gray = gray[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        maxindex = emotionDetector.detect_emotion(cropped_img)
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
        cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        streamHandler.add_frame(maxindex)
      if hasFace is not True:
        streamHandler.add_frame(7)

      if streamHandler.warning:
        print('Detected warning angry')

      img = cv2.resize(frame,(400,300),interpolation = cv2.INTER_CUBIC)
      encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
      result, img_encoded = cv2.imencode('.jpg', img, encode_param)
      data_encoded = np.array(img_encoded)
      str_encoded = data_encoded.tostring()
      print('Encoded frame')
      connection.sendall(str_encoded)
      print('Sent frame')
    sessionInfo = streamHandler.finish()
    sessionEvaluator = SessionEvaluator()
    cap.release()
    cv2.destroyAllWindows()
    # except:
    #   pass

def main():
  TestSocket().detect_from_camera()

if __name__ == '__main__':
  main()
