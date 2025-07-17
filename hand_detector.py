import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, mode =False, max_hands=1, model_complexity=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.maxHands = max_hands
        self.model_complexity = model_complexity
        self.detection_con = detection_con
        self.track_con = track_con
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity,
                                        self.detection_con, self.track_con)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

        self._land_marks = None
        self._finger_status = [0, 0, 0, 0] # [thumb, index, middle, ring, pinky] 0 if closed, 1 if open
        self.has_hand = False
        self.width = 0
        self.height = 0

    def close(self):
        self.hands.close()


    def load_hand(self, img, draw = True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        self.height, self.width, _ = img_rgb.shape

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
                self.has_hand = True
                self._land_marks = handLms
                self._update_finger_status()
                break
        else:
            self.has_hand = False

    def get_finger_status(self):
        return self._finger_status

    def _update_finger_status(self):
        if not self._land_marks:
            print("None inside counting")
            return

        self._finger_status.clear()

        thumb_tip = self._land_marks.landmark[4]
        thumb_mcp = self._land_marks.landmark[2]
        if thumb_tip.x < thumb_mcp.x:
            self._finger_status.append(1)
        else:
            self._finger_status.append(0)

        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]
        for tip_id, pip_id in zip(tips, pips):
            tip = self._land_marks.landmark[tip_id]
            pip = self._land_marks.landmark[pip_id]
            if tip.y < pip.y:  # higher up = open
                self._finger_status.append(1)
            else:
                self._finger_status.append(0)

    def is_thumbs_up(self):
        if not self._land_marks:
            print("None inside thumbs up")
            return False
        # Get landmark points
        thumb_tip = self._land_marks.landmark[4]
        thumb_ip  = self._land_marks.landmark[3]
        thumb_mcp = self._land_marks.landmark[2]

        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]

        is_thumb_up = thumb_tip.y < thumb_mcp.y

        fingers_down = True
        for tip_id, pip_id in zip(tips, pips):
            if self._land_marks.landmark[tip_id].y < self._land_marks.landmark[pip_id].y:
                fingers_down = False
                break

        return is_thumb_up and fingers_down and sum(self._finger_status) != 0 and sum(self._finger_status) == 1

    def get_finger_count(self):
        return sum(self._finger_status)
