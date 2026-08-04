# Interlace CRT picture converter

import cv2
import numpy as np
import os

def apply_scanlines_effect(image, darkness=0.4):
    result = image.astype(np.float32)
    result[1::2, :, :] *= darkness
    return np.clip(result, 0, 255).astype(np.uint8)

def process_folder(input_folder='input', output_folder='output', darkness=0.4):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    extensions = ('.jpg', '.jpeg', '.png')

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(extensions):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            img = cv2.imread(input_path)
            if img is not None:
                processed_img = apply_scanlines_effect(img, darkness)
                cv2.imwrite(output_path, processed_img)
                print(f"Processed: {filename}")
            else:
                print(f"Error: Failed to load {filename}")

process_folder('input', 'output', darkness=0.4)