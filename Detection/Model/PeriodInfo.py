class PeriodInfo:  
    def __init__(self, periodStart, periodEnd, emotion):  
        self.periodStart = periodStart
        self.periodEnd = periodEnd
        self.emotion = emotion
        self.duration = int(round((self.periodEnd-self.periodStart)*1000))

    def update(self):
        self.duration = int(round((self.periodEnd-self.periodStart)*1000))