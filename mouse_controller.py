import pyautogui
import numpy as np

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

class MouseController:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()
        self.prev_x, self.prev_y = 0, 0
        self.smoothening = 5

    def move(self, x, y, cam_w=320, cam_h=240):
        screen_x = int(np.interp(x, [50, cam_w - 50], [0, self.screen_w]))
        screen_y = int(np.interp(y, [50, cam_h - 50], [0, self.screen_h]))

        smooth_x = self.prev_x + (screen_x - self.prev_x) / self.smoothening
        smooth_y = self.prev_y + (screen_y - self.prev_y) / self.smoothening

        pyautogui.moveTo(smooth_x, smooth_y)
        self.prev_x, self.prev_y = smooth_x, smooth_y

    def left_click(self):
        pyautogui.click()

    def right_click(self):
        pyautogui.rightClick()

    def scroll_up(self):
        pyautogui.scroll(10)

    def scroll_down(self):
        pyautogui.scroll(-10)

    def double_click(self):
        pyautogui.doubleClick()