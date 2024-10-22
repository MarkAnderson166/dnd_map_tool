import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
import cv2
import threading

# Global variables
fullscreen = False
video_playing = False
current_media = None

# Directory for images and videos
image_directory = r"D:\DnD_Sidebar"  # Change this to your images directory

# --- Create Image Window ---
def create_image_window():
    global image_window, image_label
    image_window = tk.Toplevel(root)
    image_window.title("Image/Video Display")
    image_window.geometry("800x600")
    image_window.protocol("WM_DELETE_WINDOW", close_image_window)

    # Image label
    image_label = tk.Label(image_window)
    image_label.pack(fill=tk.BOTH, expand=True)

    # Bind double-click to toggle fullscreen
    image_window.bind("<Double-1>", toggle_fullscreen)

    # Create controller frame
    controller_frame = tk.Frame(root)
    controller_frame.pack(side=tk.TOP, fill=tk.X)

    # Dropdown for folders
    folder_var = tk.StringVar()
    folder_label = tk.Label(controller_frame, text="Select Folder:")
    folder_label.pack(side=tk.LEFT, padx=5)
    folder_dropdown = ttk.Combobox(controller_frame, textvariable=folder_var, state="readonly")
    folder_dropdown.pack(side=tk.LEFT, padx=5)
    
    # Load folders into the dropdown
    folders = [d for d in os.listdir(image_directory) if os.path.isdir(os.path.join(image_directory, d))]
    folder_dropdown['values'] = folders

    # Dropdown for files
    file_var = tk.StringVar()
    file_label = tk.Label(controller_frame, text="Select File:")
    file_label.pack(side=tk.LEFT, padx=5)
    file_dropdown = ttk.Combobox(controller_frame, textvariable=file_var, state="readonly")
    file_dropdown.pack(side=tk.LEFT, padx=5)

    # Load button
    load_button = ttk.Button(controller_frame, text="Load", command=lambda: load_media(folder_var.get(), file_var.get()))
    load_button.pack(side=tk.LEFT, padx=5)

# Load image or video
def load_media(folder_name, file_name):
    global current_media
    if folder_name and file_name:
        media_path = os.path.join(image_directory, folder_name, file_name)
        if file_name.endswith(('.png', '.jpg', '.jpeg')):
            load_image(media_path)
        elif file_name.endswith('.mp4'):
            play_video(media_path)

def load_image(image_path):
    global current_media
    current_media = "image"
    image = Image.open(image_path)
    image = image.resize((800, 600), Image.ANTIALIAS)  # Resize to fit the window
    current_image = ImageTk.PhotoImage(image)
    image_label.config(image=current_image)
    image_label.image = current_image

def play_video(video_path):
    global video_playing, current_media
    current_media = "video"
    video_playing = True
    cap = cv2.VideoCapture(video_path)

    def video_loop():
        while video_playing:
            ret, frame = cap.read()
            if ret:
                cv2.imshow("Video", frame)
                cv2.waitKey(1)
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video
        cap.release()
        cv2.destroyAllWindows()

    threading.Thread(target=video_loop).start()

def close_image_window():
    global video_playing
    video_playing = False
    if current_media == "video":
        cv2.destroyAllWindows()
    image_window.destroy()

def toggle_fullscreen(event):
    global fullscreen
    fullscreen = not fullscreen

    if fullscreen:
        # Get monitor dimensions based on the current window
        x = image_window.winfo_x()
        y = image_window.winfo_y()
        width = image_window.winfo_width()
        height = image_window.winfo_height()

        screen_width = image_window.winfo_screenwidth()
        screen_height = image_window.winfo_screenheight()
        image_window.geometry(f"{screen_width}x{screen_height}+0+0")
    else:
        # Restore to original size and position
        image_window.geometry("800x600")  # Or save and restore the previous dimensions

# --- Main GUI Initialization ---
root = tk.Tk()
root.title("DnD Sidebar")
create_image_window()
root.mainloop()
