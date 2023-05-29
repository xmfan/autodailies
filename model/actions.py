import pyautogui
import time
import random
import math

import constants as consts
from model.coordinate import Coordinate
from model.angle import compute_angle

# TODO: refactor below deps
from PIL import ImageGrab
CENTER = Coordinate(642, 200)
DELTA_X_90 = 257
DELTA = Coordinate(30, 0)
LEFT = CENTER - DELTA
RIGHT = CENTER + DELTA
IGNORE_THRESHOLD = 5
BIG_THRESHOLD = 20

def focus():
    # clicks a safe spot on screen
    pyautogui.click(600, 450)

noise_styles = [
    pyautogui.easeInQuad,     # start slow, end fast
    pyautogui.easeOutQuad,    # start fast, end slow
    pyautogui.easeInOutQuad,  # start and end fast, slow in middle
    pyautogui.easeInBounce,   # bounce at the end
    pyautogui.easeInElastic  # rubber band at the end
]

def drag(start: Coordinate, end: Coordinate, duration_ms: int):
    pyautogui.moveTo(start.x, start.y)
    pyautogui.dragTo(end.x, end.y, duration_ms/1000, random.choice(noise_styles), button='left')

def openMap(wait=True):
    pyautogui.click(120, 200)
    if wait: # for GUI to load
        time.sleep(1)

def closeMap(wait=True):
    pyautogui.click(1230, 110)
    if wait: # for GUI to load
        time.sleep(1)

def approx_rotate_right(degrees):
    scaling = degrees/90

    RIGHT = Coordinate(CENTER.x + (DELTA_X_90 * scaling), CENTER.y)
    focus()
    drag(CENTER, RIGHT, 500)

def approx_rotate_left(degrees):
    scaling = degrees/90

    LEFT = Coordinate(CENTER.x - (DELTA_X_90 * scaling), CENTER.y)
    focus()
    drag(CENTER, LEFT, 500)

def set_angle(current, target):
    focus()
    current += 360
    target += 360

    gap = abs(target - current)
    if target > current:
        # look left
        approx_rotate_left(target - current)
        return
    else:
        # look right
        approx_rotate_right(current - target)

def holdKey(key, duration):
    # todo: adjust based on global coordinate prediction
    pyautogui.keyDown(key)
    
    time.sleep(duration)
    pyautogui.keyUp(key)

# Maintain within 5 degrees
def keep_angle(current, target):
    focus()
    current += 360
    target += 360

    gap = abs(target - current)
    if gap < IGNORE_THRESHOLD or gap > BIG_THRESHOLD:
        return
        
    if target > current:
        # need to look left
        drag(CENTER, LEFT, 300)
    else:
        # need to look right
        drag(CENTER, RIGHT, 300)

def holdAngle(target_angle, duration = None):
    # todo: ignore bad angle frames once aligned for multiple frames
    start = time.time()
    while True:
        end = time.time()
        if duration is not None and (end - start > duration):
            break
        
        arrow = ImageGrab.grab(bbox=consts.ARROW_BBOX)
        angle = compute_angle(arrow)
        if angle:
            keep_angle(angle, target_angle)

        if duration is None:
            return

def initAngle(target_angle):
    # face FOV
    focus()
    pyautogui.keyDown('w')
    time.sleep(0.05)
    pyautogui.keyUp('w')

    # one-time angle correction
    arrow = ImageGrab.grab(bbox=consts.ARROW_BBOX)
    angle = compute_angle(arrow)
    if angle:
        set_angle(angle, target_angle)

    pyautogui.keyDown('w')
    time.sleep(0.05)
    pyautogui.keyUp('w')