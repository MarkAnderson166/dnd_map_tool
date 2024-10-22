import tkinter as tk
from tkinter import filedialog
import pygame
import os
import time
import threading

class MP3Player:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player")

        self.is_playing = False
        self.track_list = []
        self.current_track_index = -1

        pygame.mixer.init()

        self.create_widgets()

    def create_widgets(self):
        self.volume_label = tk.Label(self.root, text="Volume (0-100):")
        self.volume_label.pack()

        self.volume_scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(100)  # Default volume
        self.volume_scale.pack()

        self.load_button = tk.Button(self.root, text="Load Folder", command=self.load_folder)
        self.load_button.pack()

        self.track_listbox = tk.Listbox(self.root)
        self.track_listbox.pack(fill=tk.BOTH, expand=True)

        self.play_button = tk.Button(self.root, text="Play (with fade)", command=self.play_track)
        self.play_button.pack()

        self.pause_button = tk.Button(self.root, text="Pause (with fade)", command=self.pause_track)
        self.pause_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop (with fade)", command=self.stop_track)
        self.stop_button.pack()

        self.fade_label = tk.Label(self.root, text="Fade Duration (seconds):")
        self.fade_label.pack()

        self.fade_duration = tk.Entry(self.root)
        self.fade_duration.pack()
        self.fade_duration.insert(0, "2")  # Default fade duration

    def load_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.track_list = []
            for root, _, files in os.walk(folder_path):  # Recursively load MP3 files
                for f in files:
                    if f.endswith('.mp3'):
                        self.track_list.append(os.path.join(root, f))

            self.track_listbox.delete(0, tk.END)  # Clear the listbox
            for track in self.track_list:
                self.track_listbox.insert(tk.END, os.path.basename(track))  # Show only the file name

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(int(volume) / 100.0)

    def play_track(self):
        selected_index = self.track_listbox.curselection()
        if not selected_index:
            return

        next_track_index = selected_index[0]

        if self.is_playing:
            threading.Thread(target=self.fade_out).start()

        self.current_track_index = next_track_index
        pygame.mixer.music.load(self.track_list[self.current_track_index])
        pygame.mixer.music.play()

        threading.Thread(target=self.fade_in).start()

    def fade_in(self):
        fade_time = int(self.fade_duration.get())
        for volume in range(0, 101, 5):  # Increment volume from 0 to 100
            pygame.mixer.music.set_volume(volume / 100)
            time.sleep(fade_time / 20)  # Smooth transition

        self.is_playing = True

    def pause_track(self):
        if self.is_playing:
            threading.Thread(target=self.fade_out).start()
            pygame.mixer.music.pause()
            self.is_playing = False

    def stop_track(self):
        if self.is_playing:
            threading.Thread(target=self.fade_out).start()
            self.is_playing = False

    def fade_out(self):
        fade_time = int(self.fade_duration.get())
        for volume in range(100, -1, -5):  # Decrement volume from 100 to 0
            pygame.mixer.music.set_volume(volume / 100)
            time.sleep(fade_time / 20)  # Smooth transition
            
        pygame.mixer.music.stop()

if __name__ == "__main__":
    root = tk.Tk()
    player = MP3Player(root)
    root.mainloop()
