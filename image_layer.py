

'''
size converter
'''
import os
from PIL import Image

def process_images(input_folder, output_folder, target_size=(1920, 1080)):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Load the image
            img_path = os.path.join(input_folder, filename)
            with Image.open(img_path) as img:
                # Rotate to landscape orientation if necessary
                if img.height > img.width:
                    img = img.rotate(90, expand=True)

                # Calculate the target aspect ratio
                target_aspect_ratio = target_size[0] / target_size[1]
                img_aspect_ratio = img.width / img.height

                # Crop to the target aspect ratio
                if img_aspect_ratio > target_aspect_ratio:
                    # Image is wider than target, crop the sides
                    new_height = img.height
                    new_width = int(new_height * target_aspect_ratio)
                    img = img.crop(((img.width - new_width) // 2, 0, (img.width + new_width) // 2, new_height))
                else:
                    # Image is taller than target, crop the top and bottom
                    new_width = img.width
                    new_height = int(new_width / target_aspect_ratio)
                    img = img.crop((0, (img.height - new_height) // 2, new_width, (img.height + new_height) // 2))

                # Resize to target dimensions
                img = img.resize(target_size, Image.LANCZOS)

                # Save the processed image
                output_path = os.path.join(output_folder, filename)
                img.save(output_path)

if __name__ == "__main__":
    input_folder = "D:/DnD_Sidebar/t3"  # Change to your input folder path
    output_folder = "D:/DnD_Sidebar/t4"  # Change to your output folder path
    process_images(input_folder, output_folder)
