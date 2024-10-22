import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

# Global variables
current_color = 'black'
current_brush_size = 5
main_image = None
canvas_image = None
draw_on_main_image = None

def paint(event):
    x, y = event.x, event.y
    # Draw on the canvas
    canvas.create_oval(
        x - current_brush_size, y - current_brush_size,
        x + current_brush_size, y + current_brush_size,
        fill=current_color, outline=current_color
    )
    # Draw on the main image
    draw_on_image(x, y)

def draw_on_image(x, y):
    global draw_on_main_image
    if draw_on_main_image:
        draw_on_main_image.ellipse(
            (x - current_brush_size, y - current_brush_size, 
             x + current_brush_size, y + current_brush_size), 
            fill=current_color
        )
        update_main_image()  # Update the main image to reflect the drawing

def update_main_image():
    global canvas_image
    # Update the image in the main window to show the drawing
    main_image_tk = ImageTk.PhotoImage(main_image)
    main_image_label.config(image=main_image_tk)
    main_image_label.image = main_image_tk  # Keep a reference

def set_color(color):
    global current_color
    current_color = color

def set_brush_size(size):
    global current_brush_size
    current_brush_size = size

def clear_canvas():
    canvas.delete("all")  # Clear only the drawings from the canvas
    reset_main_image()  # Reset the main image without clearing it

def load_image():
    global main_image, draw_on_main_image, canvas_image
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if image_path:
        main_image = Image.open(image_path).resize((800, 500), Image.LANCZOS)
        canvas_image = main_image.copy()
        draw_on_main_image = ImageDraw.Draw(main_image)
        display_image()

def display_image():
    global canvas_image
    if canvas_image:
        background_image = ImageTk.PhotoImage(canvas_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
        canvas.background_image = background_image  # Keep a reference
        update_main_image()  # Display the initial image in the main window

def reset_main_image():
    global draw_on_main_image
    if main_image:
        draw_on_main_image = ImageDraw.Draw(main_image)  # Prepare for drawing again
        display_image()  # Redisplay the background image

# Set up the main drawing window
root = tk.Tk()
root.title("Simple Drawing App")
root.geometry("800x700")
root.attributes("-topmost", True)

# Create a canvas for drawing
canvas = tk.Canvas(root, bg='white', width=800, height=500)
canvas.pack()

# Bind mouse motion for drawing
canvas.bind("<B1-Motion>", paint)

# Color selection
color_label = tk.Label(root, text="Select Color:")
color_label.pack(pady=5)

color_frame = tk.Frame(root)
color_frame.pack()

colors = ['black', 'red', 'blue']
for color in colors:
    color_button = tk.Radiobutton(color_frame, text=color.capitalize(), value=color, command=lambda c=color: set_color(c))
    color_button.pack(side=tk.LEFT)

# Brush size selection
brush_size_label = tk.Label(root, text="Brush Size:")
brush_size_label.pack(pady=5)

brush_size_frame = tk.Frame(root)
brush_size_frame.pack()

brush_sizes = [5, 10, 15]
for size in brush_sizes:
    brush_size_button = tk.Radiobutton(brush_size_frame, text=str(size), value=size, command=lambda s=size: set_brush_size(s))
    brush_size_button.pack(side=tk.LEFT)

# Clear button
clear_button = tk.Button(root, text="Clear Canvas", command=clear_canvas)
clear_button.pack(pady=5)

# Load image button
load_image_button = tk.Button(root, text="Load Image", command=load_image)
load_image_button.pack(pady=5)

# Create a new window for displaying the main image
image_window = tk.Toplevel()
image_window.title("Image Display")
image_window.geometry("800x600")
image_window.attributes("-topmost", True)

# Label for main image display
main_image_label = tk.Label(image_window)
main_image_label.pack(fill=tk.BOTH, expand=True)

root.mainloop()
