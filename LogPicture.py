# Logistic map picture converter

import os
import numpy as np
from PIL import Image, ImageOps

R = 3.5
STEPS = 32
INTENSITY = 0.55

CUTOFF = 0.5
PRESERVE_TONE = True

INPUT_DIR = "input"
OUTPUT_DIR = "output"


def process_sequence():
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        print(f"Folder '{INPUT_DIR}' created. Place images inside and run the program again.")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    valid_extensions = ('.png', '.jpg', '.jpeg', '.tif', '.tiff')
    files = sorted([f for f in os.listdir(INPUT_DIR) if f.lower().endswith(valid_extensions)])

    if not files:
        print(f"No images found in '{INPUT_DIR}'.")
        return

    print("Processing images...")

    for filename in files:
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        try:
            img = Image.open(input_path).convert('RGB')
            original_data = np.array(img).astype(float) / 255.0

            x = original_data.copy()
            x = np.clip(x, 0.001, 0.999)

            for _ in range(STEPS):
                x = R * x * (1.0 - x)

            x = np.clip(x, 0.0, 1.0)

            blended_data = original_data * (1.0 - INTENSITY) + x * INTENSITY

            final_data = (blended_data * 255.0).clip(0, 255).astype(np.uint8)
            processed_img = Image.fromarray(final_data)

            optimized_img = ImageOps.autocontrast(
                processed_img,
                cutoff=CUTOFF,
                preserve_tone=PRESERVE_TONE
            )

            optimized_img.save(output_path)
            print(f"Processed: {filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print(f"\nProcessing complete. Results saved in '{OUTPUT_DIR}'.")


if __name__ == "__main__":
    process_sequence()
    input("\nPress Enter to exit...")