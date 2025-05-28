import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")

        # Initialize variables
        self.original_image = None
        self.current_image = None
        self.cropped_image = None
        self.original_photo = None
        self.cropped_photo = None
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.crop_rect = None
        self.scale_factor = 1.0

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create frames for original and cropped images
        self.original_frame = ttk.LabelFrame(self.main_frame, text="Original Image", padding="5")
        self.original_frame.grid(row=0, column=0, padx=5, pady=5)

        self.cropped_frame = ttk.LabelFrame(self.main_frame, text="Cropped Image", padding="5")
        self.cropped_frame.grid(row=0, column=1, padx=5, pady=5)

        # Create canvases for both images
        self.original_canvas = tk.Canvas(self.original_frame, width=400, height=400, bg='gray')
        self.original_canvas.grid(row=0, column=0, padx=5, pady=5)

        self.cropped_canvas = tk.Canvas(self.cropped_frame, width=400, height=400, bg='gray')
        self.cropped_canvas.grid(row=0, column=0, padx=5, pady=5)

        # Create buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.load_button = ttk.Button(self.button_frame, text="Load Image", command=self.load_image)
        self.load_button.grid(row=0, column=0, padx=5)

        self.save_button = ttk.Button(self.button_frame, text="Save Image", command=self.save_image)
        self.save_button.grid(row=0, column=1, padx=5)

        # Create resize slider
        self.resize_label = ttk.Label(self.button_frame, text="Resize:")
        self.resize_label.grid(row=0, column=2, padx=5)

        self.resize_slider = ttk.Scale(self.button_frame, from_=10, to=200, orient=tk.HORIZONTAL,
                                     command=self.resize_image)
        self.resize_slider.set(100)
        self.resize_slider.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))

        # Bind mouse events for cropping
        self.original_canvas.bind("<ButtonPress-1>", self.start_crop)
        self.original_canvas.bind("<B1-Motion>", self.update_crop)
        self.original_canvas.bind("<ButtonRelease-1>", self.end_crop)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.current_image = self.original_image.copy()
            self.cropped_image = None
            self.display_images()

    def display_images(self):
        if self.original_image is not None:
            # Display original image
            self.display_image_on_canvas(self.original_image, self.original_canvas)

            # Display cropped image if it exists
            if self.cropped_image is not None:
                self.display_image_on_canvas(self.cropped_image, self.cropped_canvas)
            else:
                self.cropped_canvas.delete("all")

    def display_image_on_canvas(self, image, canvas):
        # Get canvas dimensions
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        # Calculate scaling factor to fit image in canvas
        height, width = image.shape[:2]
        self.scale_factor = min(canvas_width/width, canvas_height/height)
        new_width = int(width * self.scale_factor)
        new_height = int(height * self.scale_factor)

        # Resize image
        resized = cv2.resize(image, (new_width, new_height))

        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(image=Image.fromarray(resized))

        # Store reference to prevent garbage collection
        if canvas == self.original_canvas:
            self.original_photo = photo
        else:
            self.cropped_photo = photo

        # Clear canvas and display image
        canvas.delete("all")
        canvas.create_image(canvas_width//2, canvas_height//2,
                          image=photo, anchor=tk.CENTER)

    def start_crop(self, event):
        self.start_x = self.original_canvas.canvasx(event.x)
        self.start_y = self.original_canvas.canvasy(event.y)
        if self.rect:
            self.original_canvas.delete(self.rect)
        self.rect = self.original_canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
        )

    def update_crop(self, event):
        cur_x = self.original_canvas.canvasx(event.x)
        cur_y = self.original_canvas.canvasy(event.y)
        self.original_canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def end_crop(self, event):
        if self.rect:
            x1, y1, x2, y2 = self.original_canvas.coords(self.rect)

            # Convert canvas coordinates to image coordinates
            x1 = int(x1 / self.scale_factor)
            y1 = int(y1 / self.scale_factor)
            x2 = int(x2 / self.scale_factor)
            y2 = int(y2 / self.scale_factor)

            # Ensure coordinates are within image bounds
            x1 = max(0, min(x1, self.original_image.shape[1]))
            y1 = max(0, min(y1, self.original_image.shape[0]))
            x2 = max(0, min(x2, self.original_image.shape[1]))
            y2 = max(0, min(y2, self.original_image.shape[0]))

            # Ensure x2 > x1 and y2 > y1
            if x2 < x1:
                x1, x2 = x2, x1
            if y2 < y1:
                y1, y2 = y2, y1

            # Crop the image
            self.cropped_image = self.original_image[y1:y2, x1:x2].copy()
            self.display_images()

    def resize_image(self, value):
        if self.cropped_image is not None:
            scale = float(value) / 100.0
            height, width = self.cropped_image.shape[:2]
            new_width = int(width * scale)
            new_height = int(height * scale)
            resized = cv2.resize(self.cropped_image, (new_width, new_height))
            self.display_image_on_canvas(resized, self.cropped_canvas)

    def save_image(self):
        if self.cropped_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if file_path:
                # Convert RGB to BGR for saving with OpenCV
                save_image = cv2.cvtColor(self.cropped_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(file_path, save_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
