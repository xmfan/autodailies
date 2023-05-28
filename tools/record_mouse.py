import csv

from pynput.mouse import Listener, Button
from pynput.keyboard import Listener as KeyboardListener, Key

FILENAME = 'mousestrokes.csv'

events = []

STOP = False

def on_move(x, y):
    events.append((x, y, 'move', None)) 

def on_click(x, y, button, pressed):
    if button == Button.left:
        events.append((x, y, 'left_click', pressed))
    elif button == Button.right:
        events.append((x, y, 'right_click', pressed))

def on_press(key):
    global STOP
    if key == Key.esc:
        STOP = True

# Create a listener for mouse events
with Listener(on_move=on_move, on_click=on_click) as listener:

    keyboard_listener = KeyboardListener(on_press=on_press)
    keyboard_listener.start()

    while not STOP:
        pass

    keyboard_listener.stop()

    with open(FILENAME, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'y', 'action', 'pressed'])
        writer.writerows(events)
