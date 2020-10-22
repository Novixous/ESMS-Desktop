import math
from Detection.emotion_stream_handler import angry_duration as ANGRY_DURATION
NO_FACE_DETECTED_DURATION = 3*60*60
emotion_dict = {7: "No face detected", 0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
negative_emotions = [0, 1, 2, 5]
positive_emotions = [3, 6]
positive_weight = 49.5
negative_weight = 50.5
class SessionEvaluator:
    def __init__(self):
        self.emotions_duration = []
        self.emotions_period_count = []
        self.negative_emotions_duration = 0
        self.positive_emotions_duration = 0
        self.neutral_emotions_duration = 0
        self.no_face_detected_duration = 0
        self.negative_emotions_period_count = 0
        self.positive_emotions_period_count = 0
        self.neutral_emotion_period_count = 0
        self.no_face_detected_period_count = 0
        self.unidentified_period_duration = 0
        self.no_face_detected_warning = 0
        self.angry_warning = 0
        self.angry_duration_warning_max = 0
        self.no_face_detected_duration_warning_max = 0
        for i in range(0, 8):
            self.emotions_duration.append(0)
            self.emotions_period_count.append(0)

    def modified_sigmoid(self, x):
        return 2 / (1 + math.exp(-0.1*x)) -1

    def evaluate(self, session_info):
        result = ""
        for periods in session_info.periods:
            for period in periods:
                self.emotions_duration[period.emotion] += period.duration
                self.emotions_period_count[period.emotion] += 1
                if period.emotion in positive_emotions:
                    self.positive_emotions_duration += period.duration
                    self.positive_emotions_period_count += 1
                elif period.emotion in negative_emotions:
                    self.negative_emotions_duration += period.duration
                    self.negative_emotions_period_count += 1
                    if period.emotion == 0:
                        if period.duration >= ANGRY_DURATION:
                            self.angry_warning += 1
                            if period.duration > self.angry_duration_warning_max:
                                self.angry_duration_warning_max = period.duration
                elif period.emotion == 4:
                    self.neutral_emotions_duration += period.duration
                    self.neutral_emotion_period_count += 1
                elif period.emotion == 7:
                    self.no_face_detected_period_count += 1
                    self.no_face_detected_duration += period.duration
                    if period.duration >= NO_FACE_DETECTED_DURATION:
                        self.no_face_detected_warning += 1
                        if period.duration > self.no_face_detected_duration_warning_max:
                            self.no_face_detected_duration_warning_max = period.duration

        session_duration = int(round((session_info.session_end - session_info.session_begin)*1000))
        self.unidentified_period_duration = session_duration - (self.negative_emotions_duration + 
        self.positive_emotions_duration + self.unidentified_period_duration + 
        self.neutral_emotions_duration + self.no_face_detected_duration)
        if self.unidentified_period_duration < 0:
            self.unidentified_period_duration = 0
        total_duration_for_estimation = session_duration - (self.no_face_detected_duration + self.unidentified_period_duration)
        neutral_duration_percentage = self.neutral_emotions_duration / session_duration
        sum_negative_positive_duration = self.negative_emotions_duration + self.positive_emotions_duration
        score = 0
        if neutral_duration_percentage < 0.50:
            if sum_negative_positive_duration != 0:
                negative_point = (self.negative_emotions_duration / sum_negative_positive_duration)*negative_weight
                positive_point = (self.positive_emotions_duration / sum_negative_positive_duration)*positive_weight
                score = self.modified_sigmoid(positive_point-negative_point)
        print("Session Duration: {}".format(session_duration))
        for i in range(0, 8):
            print("=============================================")
            print("Emotion: {}".format(emotion_dict[i]))
            print("Total Duration: {}".format(self.emotions_duration[i]))
            print("Total period count: {}".format(self.emotions_period_count[i]))
            print("*********************************************")
        print("Session Duration: {}".format(session_duration))
        print("############### Negative emotion:")
        print("Duration: {}".format(self.negative_emotions_duration))
        print("Period Count: {}".format(self.negative_emotions_period_count))
        print("############### Positive emotion:")
        print("Duration: {}".format(self.positive_emotions_duration))
        print("Period Count: {}".format(self.positive_emotions_period_count))
        print("############### Neutral emotion:")
        print("Duration: {}".format(self.neutral_emotions_duration))
        print("Period Count: {}".format(self.neutral_emotion_period_count))
        print("############### No face detected:")
        print("Duration: {}".format(self.no_face_detected_duration))
        print("Period Count: {}".format(self.no_face_detected_period_count))
        print("############### Unidentified:")
        print("Duration: {}".format(self.unidentified_period_duration))
        print("_________________result:")
        print(score)
        print(self.__dict__)

        
