import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageGrab

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

# Function to toggle the button state
def cleanup():
    button.config(text="Cleaning up")
    window.destroy()

# Create a button that toggles the boolean value
button = tk.Button(window, text="End", command=cleanup)
button.pack()

def update_overlay():
    # Capture the screen image
    screen = ImageGrab.grab()
    screen = screen.resize((256, 256))
    print(screen)

    state1.config(text='state1: test')
    state2.config(text='state2: test')

    # Schedule the next update
    window.after(1000, update_overlay)  # 1000 milliseconds = 1 second

def main():
     window.after(1000, update_overlay())

     # Start the tkinter event loop
     window.mainloop()

if __name__ == "__main__":
    main()
