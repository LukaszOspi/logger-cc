import tkinter as tk
from PIL import Image, ImageTk

def create_main_window():
    root = tk.Tk()
    root.title("Image Display Test")
    root.geometry("200x200")

    # Load an image
    try:
        image_path = "green_circle.png"  # Change this to the path of your image
        img = Image.open(image_path)
        photo_img = ImageTk.PhotoImage(img)

        # Create a label and assign the image
        label = tk.Label(root, image=photo_img)
        label.image = photo_img  # Keep a reference!
        label.pack()

    except Exception as e:
        print(f"Error loading image: {e}")

    return root

# Create and run the main window
main_window = create_main_window()
main_window.mainloop()
