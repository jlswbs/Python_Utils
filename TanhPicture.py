# Tanh saturation picture converter

import os
import numpy as np
from PIL import Image

INTENSITY = 2.1
GRAIN_AMOUNT = 0.4
INPUT_DIR = "input"
OUTPUT_DIR = "output"

def process_sequence():
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        print(f"Folder '{INPUT_DIR}' created. Please upload images and run the script again.")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    valid_extensions = ('.png', '.jpg', '.jpeg', '.tif', '.tiff')
    files = sorted([f for f in os.listdir(INPUT_DIR) if f.lower().endswith(valid_extensions)])

    if not files:
        print(f"No images found in folder '{INPUT_DIR}'.")
        return

    print(f"Starting processing of {len(files)} frames...")

    for filename in files:
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        try:
            img = Image.open(input_path).convert('RGB')
            data = np.array(img).astype(float) / 127.5 - 1.0

            saturated_data = np.tanh(data * INTENSITY)

            if GRAIN_AMOUNT > 0:
                noise = np.random.normal(0, GRAIN_AMOUNT * 0.2, saturated_data.shape)
                saturated_data += noise

            final_data = ((saturated_data + 1.0) * 127.5).clip(0, 255).astype(np.uint8)

            Image.fromarray(final_data).save(output_path)
            print(f"Done: {filename}")

        except Exception as e:
            print(f"Error processing file {filename}: {e}")

    print(f"\nProcessing completed! Files are saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_sequence()
    input("\nPress Enter to exit...")