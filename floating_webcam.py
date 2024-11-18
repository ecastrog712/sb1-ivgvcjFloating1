import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class FloatingWebcam:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Floating Webcam")
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        
        # Set window size (15% smaller than original 200x200)
        self.width = 170
        self.height = 170
        self.root.geometry(f"{self.width}x{self.height}")
        
        # Create canvas for video display
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, 
                              highlightthickness=0, bg='black')
        self.canvas.pack()
        
        # Bind mouse events for dragging
        self.canvas.bind('<Button-1>', self.start_drag)
        self.canvas.bind('<B1-Motion>', self.drag)
        
        # Add right-click menu for closing
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Close", command=self.close)
        self.root.bind('<Button-3>', self.show_menu)
        
        self.update()
        self.root.mainloop()
    
    def create_circular_mask(self, frame):
        height, width = frame.shape[:2]
        mask = np.zeros((height, width), np.uint8)
        center = (width // 2, height // 2)
        radius = min(width, height) // 2
        cv2.circle(mask, center, radius, 255, -1)
        return cv2.bitwise_and(frame, frame, mask=mask)
    
    def update(self):
        ret, frame = self.cap.read()
        if ret:
            # Resize frame
            frame = cv2.resize(frame, (self.width, self.height))
            
            # Create circular mask
            frame = self.create_circular_mask(frame)
            
            # Convert to RGB for PIL
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PhotoImage
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        self.root.after(10, self.update)
    
    def start_drag(self, event):
        self.x = event.x
        self.y = event.y
    
    def drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)
    
    def close(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    app = FloatingWebcam()