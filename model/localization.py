import cv2 as cv
from PIL import ImageGrab
import numpy as np

from model.coordinate import Coordinate

class Localizer:
    map_gray = None

    def __init__(self, map_img):
        map_cv = cv.cvtColor(np.array(map_img), cv.COLOR_RGB2BGR)
        self.map_gray = cv.cvtColor(map_cv, cv.COLOR_BGR2GRAY)
        
    def localize(self, minimap_img) -> Coordinate:
        if self.map_gray is None:
            return None

        minimap_cv = cv.cvtColor(np.array(minimap_img), cv.COLOR_RGB2BGR)
        minimap_gray = cv.cvtColor(minimap_cv, cv.COLOR_BGR2GRAY)

        result = cv.matchTemplate(self.map_gray, minimap_gray, cv.TM_CCOEFF_NORMED)
        _, confidence, _, top_left = cv.minMaxLoc(result)

        # todo: handle confidence

        position = Coordinate(
            top_left[0] + round(minimap_gray.shape[1]/2),
            top_left[1] + round(minimap_gray.shape[0]/2))

        return position
    