import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import math

# Initialize global variables
current_rotation = 0
current_image = None
fullscreen = False

# Load images from nested directories
def load_images(base_directory):
    media_dict = {}
    for root, dirs, files in os.walk(base_directory):
        folder_name = os.path.basename(root)
        media_files = [f for f in files if f.endswith(('.png', '.jpg', '.jpeg'))]
        if media_files:
            media_dict[folder_name] = media_files
    return media_dict

# Function to display the image
def show_image(folder_name, index):
    global current_image
    if folder_name in media_dict:
        media_file = media_dict[folder_name][index]
        media_path = os.path.join(media_directory, folder_name, media_file)
        current_image = Image.open(media_path)
        display_image()

# Function to display the current image with grid
def display_image():
    global current_image, current_rotation, image_label
    rotated_image = current_image.rotate(current_rotation, expand=True)
    photo = ImageTk.PhotoImage(rotated_image)
    image_label.config(image=photo)
    image_label.image = photo
    if show_grid_var.get():
        draw_grid(rotated_image)

# Rotate the image by 90 degrees
def rotate_image():
    global current_rotation
    current_rotation = (current_rotation + 90) % 360
    display_image()

# Draw grid overlay based on selected grid type
def draw_grid(image):
    grid_image = Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(grid_image)
    width, height = image.size
    grid_type = grid_type_var.get()
    x_offset = grid_x_offset_var.get()
    y_offset = grid_y_offset_var.get()
    grid_size = grid_size_var.get()

    # Clear previous grid
    draw.rectangle((0, 0, width, height), fill=(0, 0, 0, 0))

    # Set thickness and color
    thickness = grid_thickness_var.get()
    color = grid_color_var.get()

    if grid_type == 'Hexagonal':
        hex_height = int(math.sqrt(3) * grid_size)
        for row in range(int(height / hex_height) + 1):
            for col in range(int(width / (grid_size * 3 / 2)) + 1):
                x = col * grid_size * 3 / 2 + x_offset
                y = row * hex_height + (hex_height // 2 if col % 2 else 0) + y_offset
                points = [
                    (x + grid_size * math.cos(math.radians(angle)), y + grid_size * math.sin(math.radians(angle)))
                    for angle in range(0, 360, 60)
                ]
                draw.line(points + [points[0]], fill=color, width=thickness)

    elif grid_type == 'Square':
        grid_size = int(grid_size * 1.5)
        for x in range(0, width + grid_size, grid_size):
            draw.line([(x + x_offset, 0), (x + x_offset, height)], fill=color, width=thickness)
        for y in range(0, height + grid_size, grid_size):
            draw.line([(0, y + y_offset), (width, y + y_offset)], fill=color, width=thickness)

    overlay_image = Image.alpha_composite(image.convert("RGBA"), grid_image)
    photo = ImageTk.PhotoImage(overlay_image)
    image_label.config(image=photo)
    image_label.image = photo

# Toggle fullscreen mode
def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    image_window.attributes("-fullscreen", fullscreen)

# Create a window for displaying images
def create_image_window():
    global image_label, image_window
    image_window = tk.Toplevel()
    image_window.title("Image Display")
    image_window.geometry("600x800")  # Portrait aspect ratio
    image_label = tk.Label(image_window)
    image_label.pack(expand=True)
    image_label.bind("<Double-Button-1>", toggle_fullscreen)

# Set up the controller window
controller_window = tk.Tk()
controller_window.title("Image Controller")
controller_window.attributes("-topmost", True)
controller_window.geometry("400x400")

# Load media from nested directories
media_directory = r"C:\projects\DnD_Sidebar"  # Change this to your media directory
media_dict = load_images(media_directory)

# Create dropdowns for each folder
for folder in media_dict.keys():
    label = tk.Label(controller_window, text=folder)
    label.pack(pady=5)

    combo = ttk.Combobox(controller_window, values=media_dict[folder], state="readonly")
    combo.current(0)
    combo.bind("<<ComboboxSelected>>", lambda e, f=folder, c=combo: show_image(f, c.current()))
    combo.pack(pady=5)

# Rotation button on the controller
rotate_button = tk.Button(controller_window, text="Rotate 90°", command=rotate_image)
rotate_button.pack(side=tk.LEFT, padx=5, pady=5)

# Grid Controls Frame
grid_controls_frame = tk.Frame(controller_window, bd=2, relief=tk.RAISED)
grid_controls_frame.pack(pady=10, padx=10, fill=tk.BOTH)

grid_label = tk.Label(grid_controls_frame, text="Grid Controls")
grid_label.pack()

# Grid toggle button
show_grid_var = tk.BooleanVar(value=False)
toggle_grid_button = tk.Checkbutton(grid_controls_frame, text="Show Grid", variable=show_grid_var, command=display_image)
toggle_grid_button.pack(pady=5)

# Grid type selection
grid_type_var = tk.StringVar(value='Hexagonal')
grid_type_frame = tk.Frame(grid_controls_frame)
grid_type_frame.pack(pady=5)

hex_radio = tk.Radiobutton(grid_type_frame, text='Hexagonal', variable=grid_type_var, value='Hexagonal', command=display_image)
hex_radio.pack(side=tk.LEFT)

square_radio = tk.Radiobutton(grid_type_frame, text='Square', variable=grid_type_var, value='Square', command=display_image)
square_radio.pack(side=tk.LEFT)

# Slider for grid X offset
grid_x_offset_var = tk.IntVar(value=0)
grid_x_offset_slider = tk.Scale(grid_controls_frame, from_=-100, to=100, variable=grid_x_offset_var, label="X Offset", orient=tk.HORIZONTAL, command=lambda x: display_image())
grid_x_offset_slider.pack(fill=tk.X, padx=5, pady=5)

# Slider for grid Y offset
grid_y_offset_var = tk.IntVar(value=0)
grid_y_offset_slider = tk.Scale(grid_controls_frame, from_=-100, to=100, variable=grid_y_offset_var, label="Y Offset", orient=tk.HORIZONTAL, command=lambda x: display_image())
grid_y_offset_slider.pack(fill=tk.X, padx=5, pady=5)

# Slider for grid size
grid_size_var = tk.IntVar(value=40)
grid_size_slider = tk.Scale(grid_controls_frame, from_=20, to=100, variable=grid_size_var, label="Grid Size", orient=tk.HORIZONTAL, command=lambda x: display_image())
grid_size_slider.pack(fill=tk.X, padx=5, pady=5)

# Thickness selection
grid_thickness_var = tk.IntVar(value=2)
thickness_frame = tk.Frame(grid_controls_frame)
thickness_frame.pack(pady=5)

thickness_label = tk.Label(thickness_frame, text="Line Thickness:")
thickness_label.pack(side=tk.LEFT)

for thickness in [1, 2, 3]:
    thickness_radio = tk.Radiobutton(thickness_frame, text=str(thickness), variable=grid_thickness_var, value=thickness, command=display_image)
    thickness_radio.pack(side=tk.LEFT)

# Color selection
grid_color_var = tk.StringVar(value='grey')
color_frame = tk.Frame(grid_controls_frame)
color_frame.pack(pady=5)

color_label = tk.Label(color_frame, text="Line Color:")
color_label.pack(side=tk.LEFT)

for color in ['black', 'grey', 'white', 'red']:
    color_radio = tk.Radiobutton(color_frame, text=color.capitalize(), variable=grid_color_var, value=color, command=display_image)
    color_radio.pack(side=tk.LEFT)

# Create the image window
create_image_window()

# Show the initial media from the first folder
if media_dict:
    initial_folder = next(iter(media_dict))
    show_image(initial_folder, 0)

controller_window.mainloop()
