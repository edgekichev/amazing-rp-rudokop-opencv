import cv2 as cv
from win32gui import GetWindowText, GetForegroundWindow
import keyboard
from screeninfo import get_monitors
import numpy as np
from mss import mss
import time

# Разрешение

RESOLUTION = [int(x) for x in input("Введите разрешение экрана через x (Пр: 1920x1080, 1600x900, 1280x720, 2560x1440): ").split("x")]
KEY_POSITION = [int(RESOLUTION[0] * 0.47734375), int(0.733333333 * RESOLUTION[1]), int(RESOLUTION[0] * 0.04414), int(RESOLUTION[1] * 0.04097)]


DICT_FOLDER = ""
a = input("Введите папку со скриншотами (Нажмите Enter для использования папки Dict): ")
if a != "":
    DICT_FOLDER = "dict"
else:
    DICT_FOLDER = a

# Клавиши которые вы заскринили (Нужны все, скриншоты лежат в gameplay_screens)
keys = ["Down", "Left", "Right", "Up", "B", "D", "F", "H", "Q", "R", "S", "Shift", "Space", "V", "W"]

file_format = "jpg"

sct = mss()


def load():
    global bounding_box, keys_values
    screen_x, screen_y = RESOLUTION[0], RESOLUTION[1] # насрал
    # for m in get_monitors():
    #     if m.is_primary:
    #         screen_x = m.width
    #         screen_y = m.height
    bounding_box = {'top': 0, 'left': 0, 'width': screen_x, 'height': screen_y}

    keys_values = []

    for key in keys:
        key_value = []
        key_image = cv.imread(f'{DICT_FOLDER}\\{key}.{file_format}')
        gray = cv.cvtColor(key_image, cv.COLOR_BGR2GRAY)
        gray = gray[KEY_POSITION[1]:KEY_POSITION[1] + KEY_POSITION[3], KEY_POSITION[0]:KEY_POSITION[0]+KEY_POSITION[2]]
        w, h = gray.shape
        for x in range(0, h - 1):
            for y in range(0, w - 1):
                if gray[y, x] > 225:
                    key_value.append([y + KEY_POSITION[1], x + KEY_POSITION[0]])
        keys_values.append([key, key_value])


def solve_image(img):
    solve_img_values = []
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = gray[KEY_POSITION[1]:KEY_POSITION[1] + KEY_POSITION[3], KEY_POSITION[0]:KEY_POSITION[0]+KEY_POSITION[2]]
    w, h = gray.shape

    for x in range(0, h - 1):
        for y in range(0, w - 1):
            if gray[y, x] > 225:
                solve_img_values.append([y + KEY_POSITION[1], x + KEY_POSITION[0]])

    max_score = ['None', -10000]
    for key in keys_values:
        save_img = img.copy()
        score = 0
        for value in solve_img_values:
            if value in key[1]:
                score += 1
                save_img[value[0], value[1]] = (255, 0, 0)
        score = score / len(key[1])
        if max_score[1] < score:
            max_score = [key[0], score]
    return [max_score[0], int(max_score[1] * 100) / 100]


def short_solve():
    sct_img = sct.grab(bounding_box)
    screenshot = cv.cvtColor(np.array(sct_img), cv.COLOR_RGB2BGR)
    return solve_image(screenshot)

load()
if __name__ == "__main__":
    last_pressed_key = ""
    load()
    while True:
        if str(GetWindowText(GetForegroundWindow())).find("AMAZING ONLINE") != -1:
            solved = short_solve()
            if solved[1] > 0.9:
                keyboard.press(solved[0].lower())
                last_pressed_key = solved[0].lower()

                while solved[0].lower() == last_pressed_key:
                    time.sleep(0.25)
                    solved = short_solve()
                keyboard.release(solved[0].lower())
            time.sleep(0.1)