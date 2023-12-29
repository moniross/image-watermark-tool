import os
from PIL import Image, ImageTk
from tkinter import messagebox

def add_watermark(input_image_path, output_image_path, watermark_path, opacity=1.0, selected_position="bottom_right"):
    original_image = Image.open(input_image_path)
    watermark = Image.open(watermark_path).resize((200, 70))


    # Calculate the position based on the selected option
    if "left" in selected_position:
        x_position = 10
        y_position = (original_image.size[1] - watermark.size[1]) // 2
        output_image_path = output_image_path.replace(".", f"_left.")
    elif "right" in selected_position:
        x_position = original_image.size[0] - watermark.size[0] - 10
        y_position = (original_image.size[1] - watermark.size[1]) // 2
        output_image_path = output_image_path.replace(".", f"_right.")
    elif "top" in selected_position:
        x_position = (original_image.size[0] - watermark.size[0]) // 2
        y_position = 10
        output_image_path = output_image_path.replace(".", f"_top.")
    elif "bottom" in selected_position:
        x_position = (original_image.size[0] - watermark.size[0]) // 2
        y_position = original_image.size[1] - watermark.size[1] - 10
        output_image_path = output_image_path.replace(".", f"_bottom.")
    elif "center" in selected_position:
        x_position = (original_image.size[0] - watermark.size[0]) // 2
        y_position = (original_image.size[1] - watermark.size[1]) // 2
        output_image_path = output_image_path.replace(".", f"_center.")
    elif "bottom_center" in selected_position:
        x_position = (original_image.size[0] - watermark.size[0]) // 2
        y_position = original_image.size[1] - watermark.size[1] - 10
        output_image_path = output_image_path.replace(".", f"_bottom_center.")
    elif "top_center" in selected_position:
        x_position = (original_image.size[0] - watermark.size[0]) // 2
        y_position = 10
        output_image_path = output_image_path.replace(".", f"_top_center.")
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
