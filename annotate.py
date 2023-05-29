from pynput import keyboard
import pyautogui
import cv2 as cv
from typing import List
from PIL import ImageGrab, Image
import numpy as np
import math

from model.coordinate import Coordinate
from model.angle import compute_line_angle
from model.actions import openMap, closeMap
import constants as consts

def grabMap() -> Image.Image:
    return ImageGrab.grab((
        consts.MAP_TOP_LEFT.x,
        consts.MAP_TOP_LEFT.y,
        consts.MAP_BOTTOM_RIGHT.x,
        consts.MAP_BOTTOM_RIGHT.y))

def annotate() -> List[Coordinate]:
    coords = []

    # Callback function to handle key press events
    def on_press(key):
        nonlocal coords
        
        # Stop the listener if the Escape key is pressed
        if key == keyboard.Key.esc:
            return False
    
        x, y = pyautogui.position()
        coords.append(Coordinate(x,y))

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    # Keep the program running until the listener is stopped
    listener.join()
    
    return coords


def save(map_img: Image.Image , coords: List[Coordinate]) -> None:
    if len(coords) < 2:
        print('No path to save')
        return
    
    # offset
    display_coords: List[Coordinate] = []
    for coord in coords:
        display_coords.append(coord - consts.MAP_TOP_LEFT)
        
    map_cv = cv.cvtColor(np.array(map), cv.COLOR_RGB2BGR)

    filename = input("Save as routine/{filename}.csv, filename: ")
    path = f"routines/{filename}.csv"
    with open(path, 'w') as f:
        f.write('angle,dist\n')
        
        start = display_coords[0]
        for end in display_coords[1:]:
            angle = compute_line_angle(start.asTuple(), end.asTuple()) * -1
            dist = math.sqrt((end.x - start.x)**2 + (end.y - start.y)**2)
    
            f.write(f"{angle},{dist}\n")
            
            cv.arrowedLine(map_cv, start.asTuple(), end.asTuple(), (255, 0, 0), thickness=2)
            start = end

    img_path = f"routines/imgs/{filename}.jpg"
    cv.imwrite(img_path, cv.cvtColor(map_cv, cv.COLOR_BGR2RGB))
    print(f"Written to {img_path}")

    
"""
Annotate a map, and store the paths under routines/
"""
if __name__ == "__main__":
    openMap()
    map = grabMap()
    coords = annotate()
    closeMap()
    save(map, coords)