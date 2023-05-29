import threading

from model.actions import focus, initAngle, holdKey, holdAngle
from PIL import Image
from model.coordinate import Coordinate
from model.routine import Routine
import constants as consts

class Agent:
    def __init__(self):
        pass

    def act(self, angle: float, environment: Image.Image, position: Coordinate) -> None:
        pass

    def runRoutine(self, path):
        routine = Routine(path)

        inst = routine.next()
        while inst is not None:
            print(f"Running next instruction: {inst}")
            target_angle = inst.angle
            duration = inst.dist / consts.PIXELS_PER_SECOND

            KeyboardThread = threading.Thread(target=holdKey, args=('w', duration,))
            MouseThread = threading.Thread(target=holdAngle, args=(target_angle, duration,))

            initAngle(target_angle)
            KeyboardThread.start()
            MouseThread.start()
            
            KeyboardThread.join()
            MouseThread.join()
            
            inst = routine.next()

        print(f"Done running routine")