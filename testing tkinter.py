import tkinter as tk
from PIL import Image, ImageTk


def remove_image():
    label.configure(image="")
    label.config(width=image_width, height=image_height)


# Create the tkinter window
window = tk.Tk()

# Load the image
image = Image.open(
    r"images/mine.png"
)  # Replace "image.png" with the actual path to your image
photo = ImageTk.PhotoImage(image)

# Get the dimensions of the image
image_width = image.width
image_height = image.height

# Create a label with the image
label = tk.Label(window, image=photo, width=image_width, height=image_height)
label.pack()

# Create a button to remove the image
button = tk.Button(window, text="Remove Image", command=remove_image)
button.pack()

# Run the tkinter event loop
window.mainloop()
