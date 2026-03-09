import cv2
import mediapipe as mp
import math

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.9,
            min_tracking_confidence=0.9,
            model_complexity=1
        )
        self.results = None

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks and draw:
            for hand in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_landmark(self, img, landmark_id):
        h, w, _ = img.shape
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            lm = hand.landmark[landmark_id]
            return int(lm.x * w), int(lm.y * h)
        return None

    def is_index_up(self):
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            landmarks = hand.landmark
            index_up    = landmarks[8].y  < landmarks[6].y
            middle_down = landmarks[12].y > landmarks[10].y
            ring_down   = landmarks[16].y > landmarks[14].y
            pinky_down  = landmarks[20].y > landmarks[18].y
            return index_up and middle_down and ring_down and pinky_down
        return False

    def is_pinch(self):
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            landmarks = hand.landmark
            dist = math.hypot(
                landmarks[4].x - landmarks[8].x,
                landmarks[4].y - landmarks[8].y
            )
            return dist < 0.07
        return False

    def is_peace(self):
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            landmarks = hand.landmark
            index_up   = landmarks[8].y  < landmarks[6].y
            middle_up  = landmarks[12].y < landmarks[10].y
            ring_down  = landmarks[16].y > landmarks[14].y
            pinky_down = landmarks[20].y > landmarks[18].y
            return index_up and middle_up and ring_down and pinky_down
        return False

    def is_fist(self):
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            landmarks = hand.landmark
            finger_tips = [8, 12, 16, 20]
            finger_base = [6, 10, 14, 18]
            curled = 0
            for tip, base in zip(finger_tips, finger_base):
                if landmarks[tip].y > landmarks[base].y:
                    curled += 1
            return curled == 4
        return False