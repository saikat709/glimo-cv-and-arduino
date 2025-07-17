import cv2
from hand_detector import HandDetector
from device_controller import control_leds

WINDOW_NAME = "Glimo"
WIDTH       = 840
HEIGHT      = 640

def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"🖱️ Click at: ({x}, {y})")


def main():
    
    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, on_mouse)

    cap = cv2.VideoCapture(0)

    hand_detector = HandDetector()

    while True:
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.resize(image, (WIDTH, HEIGHT))
        image = cv2.flip(image, 1)
        hand_detector.load_hand(image)
        finger_status = hand_detector.get_finger_status()
        
        cnt = sum(finger_status)
        cv2.putText(image, f"Fingers: {cnt}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if finger_status:
            control_leds(finger_status)

        cv2.imshow(WINDOW_NAME, image)
        key = cv2.waitKey(1)

        if key & 0xFF == ord('q') or key == 27 or cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            break

    hand_detector.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print("Application started...")

    main()