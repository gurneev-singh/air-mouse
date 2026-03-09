import cv2
import time
from hand_tracker import HandTracker
from mouse_controller import MouseController
from utils import draw_status, draw_cursor_point

tracker = HandTracker()
mouse = MouseController()

cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)

cv2.namedWindow("Air Mouse")
cv2.moveWindow("Air Mouse", 0, 0)

last_click_time = 0
last_right_click_time = 0
last_scroll_time = 0
COOLDOWN = 0.3

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img = tracker.find_hands(img)
    current_time = time.time()

    gesture = "none"

    # pinch = left click (checked FIRST)
    if tracker.is_pinch():
        if current_time - last_click_time > COOLDOWN:
            mouse.left_click()
            last_click_time = current_time
            gesture = "left click"

    # index finger up = move cursor
    elif tracker.is_index_up():
        index_pos = tracker.get_landmark(img, 8)
        if index_pos:
            x, y = index_pos
            draw_cursor_point(img, x, y)
            mouse.move(x, y, cam_w=320, cam_h=240)
            gesture = "moving"

    # peace = right click
    elif tracker.is_peace():
        if current_time - last_right_click_time > COOLDOWN:
            mouse.right_click()
            last_right_click_time = current_time
            gesture = "right click"

    # fist = scroll
    elif tracker.is_fist():
        fist_pos = tracker.get_landmark(img, 9)
        if fist_pos:
            _, y = fist_pos
            if current_time - last_scroll_time > 0.05:
                if y < 100:
                    mouse.scroll_up()
                elif y > 150:
                    mouse.scroll_down()
                last_scroll_time = current_time
            gesture = "scrolling"

    draw_status(img, gesture, "air mouse")

    cv2.imshow("Air Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()