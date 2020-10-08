import time
from datetime import datetime
from Detection.Model.FrameInfo import FrameInfo
from Detection.Model.PeriodInfo import PeriodInfo
from Detection.Model.SessionInfo import SessionInfo
emotion_dict = {7: "No face detected", 0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
# duration in miliseconds to be considered a valid emotion period
emotion_valid_duration = {7: 4000,0: 250, 1: 250, 2: 250, 3: 500, 4: 500, 5: 250, 6: 500}
emotion_maximum_buffer_duration = {7: 300, 0: 400, 1: 400, 2: 400, 3: 300, 4: 300, 5: 300, 6: 300}
class EmotionStreamHandler:
    def __init__(self):
        self.frames = []
        self.currentFrame = FrameInfo(None, None, None)
        self.previousFrame = FrameInfo(None, None, None)
        self.periods = []
        self.tempDurations = []
        for i in range (0, 8):
            self.periods.append([])
            self.tempDurations.append([0,0])
        self.beginSession = 0
        self.tempTime = 0
        self.count = 0
    
    def addFrame(self, emotion):

        if self.beginSession == 0:
            self.beginSession = time.time()
        
        self.tempTime = time.time()
        
        passedTime = int(round((self.tempTime - self.beginSession)*1000))

        self.currentFrame = FrameInfo(self.tempTime, passedTime, emotion)
        self.count+=1
        if self.previousFrame.timeStamp is not None:
            for i in range(0, 8):
                duration = int(round((self.currentFrame.timeStamp - self.previousFrame.timeStamp)*1000))
                if self.previousFrame.emotion == i and self.tempDurations[i] == [0,0]:
                    self.periods[i].append(PeriodInfo(self.previousFrame.timeStamp, self.currentFrame.timeStamp, i))
                    self.tempDurations[i][0] += duration
                elif self.previousFrame.emotion == i and self.tempDurations[i] != [0,0]:
                    self.tempDurations[i][0] += duration
                    self.periods[i][len(self.periods[i])-1].periodEnd = self.currentFrame.timeStamp
                    self.periods[i][len(self.periods[i])-1].update()
                    self.tempDurations[i][1] = 0
                elif self.previousFrame.emotion != i and self.tempDurations[i] == [0,0]:
                    pass
                elif self.previousFrame.emotion != i and self.tempDurations[i] != [0,0]:
                    if self.tempDurations[i][0] >= emotion_valid_duration[i]:
                        self.tempDurations[i][1] += duration
                        if self.tempDurations[i][1] >= emotion_maximum_buffer_duration[i]:
                            self.tempDurations[i] = [0,0]
                    else:                        
                        self.tempDurations[i] = [0,0]
                        duration = int(round((self.periods[i][len(self.periods[i])-1].periodEnd - self.periods[i][len(self.periods[i])-1].periodStart)*1000))
                        del(self.periods[i][len(self.periods[i])-1])
        self.previousFrame = self.currentFrame
    def finish(self):
        

        for i in range(0, len(self.periods)):
            if len(self.periods[i]) > 0:
                if self.periods[i][len(self.periods[i])-1].duration < emotion_valid_duration[i]:
                    del(self.periods[i][len(self.periods[i])-1])
        # ****** print out all periods ******
        # for i in range(0, len(self.periods)):
        #     print("===={}==== size: {}".format(emotion_dict[i], len(self.periods[i])))
        #     for period in self.periods[i]:
        #         print(period.__dict__)
        #         duration = int(round((period.periodEnd - period.periodStart)*1000))
        # print("__________________________________________________________________________________________")
        # print("__________________________________________________________________________________________")
        sessionInfo = SessionInfo(self.frames, self.beginSession, self.tempTime, self.periods) 
        return sessionInfo
