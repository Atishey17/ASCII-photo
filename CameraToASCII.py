import cv2
import tkinter as tk
from PIL import Image, ImageTk

#CHARS = "@%#*+=-:. "
CHARS=" .:░▒▓█"

def setup():
    global video, root, asci_label
    root = tk.Tk()
    root.title("Video to ASCII Art")
    root.geometry("{0}x{1}".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    asci_label = tk.Label(root, font=("Courier New", 8), bg="black", fg="white")
    asci_label.pack(fill=tk.BOTH, expand=True)

    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 80)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 80)

    update_ascii_image()
    root.protocol("WM_DELETE_WINDOW", exit_program)
    root.mainloop()

def draw():
    ret, frame = video.read()
    if not ret:
        return

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = Image.fromarray(gray_frame)

    asci_image = convert_image_to_ascii(image, 160)
    return asci_image

def convert_image_to_ascii(image, cols, padding=10):
    scale = image.size[1] / image.size[0]
    width = cols
    height = int(scale * width)
    image = image.resize((width, height))
    ascii_image = ""
    for y in range(height):
        ascii_line = ""
        for _ in range(padding):
            ascii_line += " "
        for x in range(width):
            pixel = image.getpixel((x, y))
            pixel_index = int((pixel / 255) * (len(CHARS) - 1))
            ascii_line += CHARS[pixel_index]
        for _ in range(padding):
            ascii_line += " "
        ascii_line += "\n"
        ascii_image += ascii_line
    return ascii_image

def update_ascii_image():
    asci_art = draw()
    asci_label.config(text=asci_art)
    root.after(50, update_ascii_image)
  
def exit_program():
    global video
    if video is not None:
        video.release()
    if root is not None:
        root.destroy()
      
setup()
