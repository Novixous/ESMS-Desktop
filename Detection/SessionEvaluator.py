emotion_dict = {7: "No face detected", 0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
negative_emotions = [0, 1, 2, 5]
positive_emotions = [3, 6]
class SessionEvaluator:
    def __init__(self):
        self.emotionsDuration = []
        self.emotionsPeriodCount = []
        self.negativeEmotionsDuration = 0
        self.positiveEmotionsDuration = 0
        for i in range(0, 8):
            self.emotionsDuration.append(0)
            self.emotionsPeriodCount.append(0)

    def evaluate(self, sessionInfo):
        result = ""
        for periods in sessionInfo.periods:
            for period in periods:
                self.emotionsDuration[period.emotion] += period.duration
                self.emotionsPeriodCount[period.emotion] += 1
                if period.emotion in positive_emotions:
                    self.positiveEmotionsDuration += period.duration
                elif period.emotion in negative_emotions:
                    self.negativeEmotionsDuration += period.duration
        sessionDuration = int(round((sessionInfo.sessionEnd - sessionInfo.sessionBeggin)*1000))
        print("Session Duration: {}".format(sessionDuration))
        for i in range(0, 8):
            print("=============================================")
            print("Emotion: {}".format(emotion_dict[i]))
            print("Total Duration: {}".format(self.emotionsDuration[i]))
            print("Total period count: {}".format(self.emotionsPeriodCount[i]))
            print("*********************************************")
        if self.negativeEmotionsDuration > int(round(sessionDuration/100*35)):
            result += "Your expression is negative toward the customer.\n"
        elif self.negativeEmotionsDuration <= int(round(sessionDuration/100*35)):
            if self.negativeEmotionsDuration > int(round(sessionDuration/100*20)):
                result += "Your expression is quite negative toward the customer.\n"
            if self.emotionsDuration[4] > int(round(sessionDuration/100*90)):
                result += "Your face through out the session seem to be emotionless.\nPlease try to be more cheerful toward customer.\n"
            if self.emotionsDuration[7] > int(round(sessionDuration/100*60)):
                result += "You did not interact with the customer for more than 60 percent of the time.\n Please try not to leave for too long.\n"
        else:
            if self.positiveEmotionsDuration > int(round(sessionDuration/100*30)):
                result += "Great job keep up with that attitude.\n"
            else:
                result += "Everything was alright.\n"
        print(result)
        return result
