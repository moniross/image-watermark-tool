import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from queue import Queue
from threading import Thread

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

def add_watermark(input_image_path, output_image_path, watermark_path, opacity=1.0, selected_position="bottom_right"):
    original_image = Image.open(input_image_path)
    watermark = Image.open(watermark_path).resize((200, 70))

    # Calculate the position based on the selected option
    if "left" in selected_position:
        x_position = 10
        y_position = (original_image.size[1] - watermark.size[1]) // 2
    elif "right" in selected_position:
        x_position = original_image.size[0] - watermark.size[0] - 10
        y_position = (original_image.size[1] - watermark.size[1]) // 2
    elif "top" in selected_position:
        x_position = (original_image.size[0] - watermark.size[0]) // 2
        y_position = 10
    elif "bottom" in selected_position:
        x_position = (original_image.size[0] - watermark.size[0]) // 2
        y_position = original_image.size[1] - watermark.size[1] - 10
    elif "center" in selected_position:
        x_position = (original_image.size[0] - watermark.size[0]) // 2
        y_position = (original_image.size[1] - watermark.size[1]) // 2
    elif "bottom_center" in selected_position:
        x_position = (original_image.size[0] - watermark.size[0]) // 2
        y_position = original_image.size[1] - watermark.size[1] - 10
    elif "top_center" in selected_position:
        x_position = (original_image.size[0] - watermark.size[0]) // 2
        y_position = 10
    else:
        raise ValueError(f"Invalid position: {selected_position}")

    watermark_position = (x_position, y_position)

    watermark_overlay = Image.new('RGBA', original_image.size, (0, 0, 0, 0))
    watermark_overlay.paste(watermark, watermark_position, watermark)
    watermarked_image = Image.alpha_composite(original_image.convert('RGBA'), watermark_overlay)

    watermarked_image = watermarked_image.convert('RGB')
    watermarked_image.save(output_image_path)

def watermark_images_in_folder(folder_path, watermark_path, opacity=1.0, selected_position="bottom_right"):
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")

    if not os.path.exists(watermark_path):
        raise FileNotFoundError(f"The watermark image '{watermark_path}' does not exist.")

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for file_name in files:
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            input_image_path = os.path.join(folder_path, file_name)
            output_image_path = os.path.join(folder_path, f"watermarked_{file_name}")

            if not file_name.startswith("watermarked_"):
                add_watermark(input_image_path, output_image_path, watermark_path, opacity, selected_position)
                print(f"Watermarked: {file_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
