import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from image_processing import watermark_images_in_folder

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App")

        self.folder_path = tk.StringVar()
        self.watermark_path = tk.StringVar()
        self.opacity = tk.DoubleVar(value=1.0)
        self.selected_position = tk.StringVar(value="bottom_right")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select Assets Folder:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(self.root, textvariable=self.folder_path, state="readonly", width=50).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_folder).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.root, text="Select Watermark PNG:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(self.root, textvariable=self.watermark_path, state="readonly", width=50).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_watermark).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(self.root, text="Opacity (0.0 to 1.0):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(self.root, textvariable=self.opacity).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Select Watermark Position:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.OptionMenu(self.root, self.selected_position, "left", "right", "top", "bottom", "center", "bottom_center", "top_center").grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Watermark Images", command=self.watermark_images).grid(row=4, column=1, pady=10)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path.set(folder_path)

    def browse_watermark(self):
        watermark_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if watermark_path:
            self.watermark_path.set(watermark_path)

    def watermark_images(self):
        folder_path = self.folder_path.get()
        watermark_path = self.watermark_path.get()
        opacity = self.opacity.get()
        selected_position = self.selected_position.get()

        if not folder_path or not watermark_path:
            messagebox.showerror("Error", "Please select the assets folder and watermark PNG.")
            return

        try:
            watermark_images_in_folder(folder_path, watermark_path, opacity, selected_position)
            messagebox.showinfo("Success", "Watermarking completed.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
