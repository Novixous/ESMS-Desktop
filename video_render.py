import cv2
import json
from time import sleep
from Detection.Model.frame_info import FrameInfo
frames_file_info = open("data.json", "r")
frames_infos = json.loads(frames_file_info.read())
cap = cv2.VideoCapture('temp_vid.mp4')
current_time_eslapsed = 0
current_index = 0
while(cap.isOpened()):
  ret, frame = cap.read()

  if current_index <= len(frames_infos) - 1:
    waiting_time = (int(frames_infos[current_index]['time_eslaped']) - current_time_eslapsed)/1000
    current_time_eslapsed = int(frames_infos[current_index]['time_eslaped'])
    current_index+=1
    sleep(waiting_time)
    print(waiting_time)
    cv2.imshow('Video',frame)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
  if not ret:
    break

cap.release()
cv2.destroyAllWindows()