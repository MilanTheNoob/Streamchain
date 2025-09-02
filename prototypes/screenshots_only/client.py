import tkinter as tk
from tkinter import simpledialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import threading
import mss
import cv2
import numpy as np
import requests
import time
import io

SERVER_URL = 'http://localhost:5000'

class StreamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📺 Stream & View")
        self.frame = tb.Frame(root, padding=20)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Container for image
        self.image_label = tk.Label(self.frame, bg="black", text="Stream Preview Appears Here", fg="white")
        self.image_label.pack(pady=10)

        # Button row
        btn_frame = tb.Frame(self.frame)
        btn_frame.pack(pady=10)

        self.stream_button = tb.Button(btn_frame, text="Start Streaming", bootstyle=PRIMARY, command=self.toggle_stream)
        self.stream_button.pack(side=tk.LEFT, padx=5)
        tb.Button(btn_frame, text="View Stream", bootstyle=SUCCESS, command=self.start_viewer).pack(side=tk.LEFT, padx=5)

        self.running_viewer = False
        self.streaming = False
        self.last_photo = None

    def toggle_stream(self):
        if self.streaming:
            self.streaming = False
            self.running_viewer = False
            self.stream_button.config(text="🎥 Start Streaming", bootstyle=PRIMARY)
        else:
            stream_id = simpledialog.askstring("Stream ID", "Enter an ID for your stream:")
            if stream_id:
                self.streaming = True
                self.stream_button.config(text="Stop Streaming", bootstyle=DANGER)
                self.stream_thread = threading.Thread(target=self.stream_screen, args=(stream_id,), daemon=True)
                self.stream_thread.start()

    def stream_screen(self, stream_id):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            while self.streaming:
                img = np.array(sct.grab(monitor))
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
                try:
                    requests.post(
                        f"{SERVER_URL}/upload",
                        data={'stream_id': stream_id},
                        files={'frame': buffer.tobytes()}
                    )

                    self.start_viewer(stream_id)
                except Exception as e:
                    print("Stream failed:", e)
                time.sleep(0.05)

    def start_viewer(self, stream_id=None):
        if stream_id is None:
            stream_id = simpledialog.askstring("View Stream", "Enter stream ID to view:")
        if stream_id:
            self.running_viewer = True
            threading.Thread(target=self.view_stream, args=(stream_id,), daemon=True).start()

    def view_stream(self, stream_id):
        while self.running_viewer:
            try:
                res = requests.get(f"{SERVER_URL}/latest/{stream_id}", timeout=5)
                if res.status_code == 200:
                    img_data = res.content
                    image = Image.open(io.BytesIO(img_data)).convert("RGB")

                    # Resize to fit a max width
                    max_width = 800
                    w_percent = (max_width / float(image.size[0]))
                    h_size = int((float(image.size[1]) * float(w_percent)))
                    image = image.resize((max_width, h_size), Image.LANCZOS)

                    photo = ImageTk.PhotoImage(image)
                    self.image_label.config(image=photo, text="")
                    self.last_photo = photo
            except Exception as e:
                print("Viewer failed:", e)
            time.sleep(0.05)

if __name__ == "__main__":
    app = tb.Window(themename="superhero")
    stream_app = StreamApp(app)
    app.geometry("850x600")
    app.mainloop()
