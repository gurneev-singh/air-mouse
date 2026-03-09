import cv2

def draw_status(img, gesture, mode):
    cv2.putText(img, f"Gesture: {gesture}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, f"Mode: {mode}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

def draw_cursor_point(img, x, y):
    cv2.circle(img, (x, y), 10, (255, 0, 255), -1)
    cv2.circle(img, (x, y), 15, (255, 0, 255), 2)