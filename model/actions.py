import pyautogui
import time

def focus():
    # clicks a safe spot on screen
    pyautogui.click(600, 450)

def openMap(wait=True):
    pyautogui.click(120, 200)
    if wait: # for GUI to load
        time.sleep(1)

def closeMap(wait=True):
    pyautogui.click(1230, 110)
    if wait: # for GUI to load
        time.sleep(1)
    
class ActionBase:
    def __init__(self):
        pass
