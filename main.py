import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageGrab
import pyautogui
import time

from model.agent import Agent
from model.angle import compute_angle
from model.localization import Localizer
from model.coordinate import Coordinate

# Only supports 720p
Y_OFFSET = 72 # Mac UIs
GAME_TOP_LEFT_X = 0
GAME_TOP_LEFT_Y = Y_OFFSET
GAME_WIDTH = 1280
GAME_HEIGHT = 720
GAME_BBOX = (
    GAME_TOP_LEFT_X,
    GAME_TOP_LEFT_Y,
    GAME_TOP_LEFT_X + GAME_WIDTH,
    GAME_TOP_LEFT_Y + GAME_HEIGHT)

MINIMAP_CENTER = Coordinate(117,200)
MINIMAP_PAD = Coordinate(55,55)
MINIMAP_TOP_LEFT = MINIMAP_CENTER - MINIMAP_PAD
MINIMAP_BOTTOM_RIGHT = MINIMAP_CENTER + MINIMAP_PAD
MINIMAP_BBOX = (
    MINIMAP_TOP_LEFT.x,
    MINIMAP_TOP_LEFT.y,
    MINIMAP_BOTTOM_RIGHT.x,
    MINIMAP_BOTTOM_RIGHT.y)

MAP_TOP_LEFT_X = 100
MAP_TOP_LEFT_Y = Y_OFFSET
MAP_BOTTOM_RIGHT_X = 860
MAP_BOTTOM_RIGHT_Y = 720 + Y_OFFSET
MAP_BBOX = (
    MAP_TOP_LEFT_X,
    MAP_TOP_LEFT_Y,
    MAP_BOTTOM_RIGHT_X,
    MAP_BOTTOM_RIGHT_Y)

ARROW_TOP_LEFT_X = 105
ARROW_TOP_LEFT_Y = 185
ARROW_BOTTOM_RIGHT_X = 130
ARROW_BOTTOM_RIGHT_Y = 210
ARROW_BBOX = (
    ARROW_TOP_LEFT_X,
    ARROW_TOP_LEFT_Y,
    ARROW_BOTTOM_RIGHT_X,
    ARROW_BOTTOM_RIGHT_Y)

# Create a tkinter window
window = tk.Tk()

# Set the window attributes
window.attributes('-topmost', True)  # Keep the window on top
window.overrideredirect(True)  # Remove the window decorations (title bar, borders, etc.)

# Get the screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the coordinates for the top-right corner
overlay_width = 300 # Adjust the width of the overlay window as needed
overlay_height = 600 # Adjust the height of the overlay window as needed
x_coordinate = screen_width - overlay_width
y_coordinate = 0

# Set the geometry of the window to the top-right corner
window.geometry(f"{overlay_width}x{overlay_height}+{x_coordinate}+{y_coordinate}")

# Create a transparent overlay frame
overlay_frame = tk.Frame(window, bg='black')
overlay_frame.place(relx=1, anchor='ne')
overlay_frame.pack()

# Add the label with the desired text
title = tk.Label(overlay_frame, text='autodailies running', fg='white', bg='black')
title.pack(padx=10, pady=10)

state1 = tk.Label(overlay_frame, text='state1: 0', fg='white', bg='blue')
state1.pack()
state2 = tk.Label(overlay_frame, text='state2: 0', fg='white', bg='blue')
state2.pack()

# Function on button click
def cleanup():
    button.config(text="Cleaning up")
    window.destroy()

# Create a button that toggles the boolean value
button = tk.Button(window, text="End", command=cleanup)
button.pack()

agent = Agent()
localizer = None

def activate():
    pyautogui.click(600, 450)

def init():
    global localizer
    activate()
    pyautogui.click(MINIMAP_CENTER.x, MINIMAP_CENTER.y)
    time.sleep(2)
    map_img = ImageGrab.grab(bbox=MAP_BBOX)
    localizer = Localizer(map_img)
    pyautogui.click(1230, 110)
    window.after(2000, run)

def run():
    global localizer
    arrow_img = ImageGrab.grab(bbox=ARROW_BBOX)
    angle = compute_angle(arrow_img)

    minimap_img = ImageGrab.grab(bbox=MINIMAP_BBOX)
    position: Coordinate = localizer.localize(minimap_img)
    # action = agent.choose_action(screen)

    state1.config(text=f"orientation: {angle}")
    state2.config(text=f"({position.x}, {position.y})")

    # Schedule the next update
    window.after(100, run)  # 1000 milliseconds = 1 second

def main():
     window.after(100, init)

     # Start the tkinter event loop
     window.mainloop()

if __name__ == "__main__":
    main()
