import time
from datetime import datetime
from Detection.Model.FrameInfo import FrameInfo
from Detection.Model.PeriodInfo import PeriodInfo
from Detection.Model.SessionInfo import SessionInfo
NO_FACE_DETECTED = 7
ANGRY = 0
DISGUSTED = 1
FEARFUL = 2
HAPPY = 3
NEUTRAL = 4
SAD = 5
SURPRISED = 6
emotion_dict = {NO_FACE_DETECTED: "No face detected", ANGRY: "Angry", DISGUSTED: "Disgusted", FEARFUL: "Fearful", HAPPY: "Happy", 
NEUTRAL: "Neutral", SAD: "Sad", SURPRISED: "Surprised"}

# duration in miliseconds to be considered a valid emotion period
emotion_valid_duration = {
    NO_FACE_DETECTED: 4000, 
    ANGRY: 250, 
    DISGUSTED: 250, 
    FEARFUL: 250, 
    HAPPY: 500, 
    NEUTRAL: 1000, 
    SAD: 250, 
    SURPRISED: 500}
emotion_maximum_buffer_duration = {
    NO_FACE_DETECTED: 300, 
    ANGRY: 1500, 
    DISGUSTED: 400, 
    FEARFUL: 400, 
    HAPPY: 300, 
    NEUTRAL: 300, 
    SAD: 300, 
    SURPRISED: 300}

angry_duration = 5000
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
        self.warning = False
    
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
                    if i == ANGRY:
                        if self.periods[i][len(self.periods[i])-1].duration >= angry_duration:
                            self.warning = True
                elif self.previousFrame.emotion != i and self.tempDurations[i] == [0,0]:
                    pass
                elif self.previousFrame.emotion != i and self.tempDurations[i] != [0,0]:
                    if self.tempDurations[i][0] >= emotion_valid_duration[i]:
                        self.tempDurations[i][1] += duration
                        if self.tempDurations[i][1] >= emotion_maximum_buffer_duration[i]:
                            self.tempDurations[i] = [0,0]
                            if self.warning == True:
                                self.warning = False
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
        for periods in self.periods:
            for period in periods:
                period.periodStart = int(round((period.periodStart - self.beginSession)*1000))
                period.periodEnd = int(round((period.periodEnd - self.beginSession)*1000))
        sessionInfo = SessionInfo(self.frames, self.beginSession, self.tempTime, self.periods) 
        return sessionInfo
