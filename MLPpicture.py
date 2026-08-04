# MLP network picture converter

import os
import numpy as np
from PIL import Image

WEIGHT_INIT = 1.5
HIDDEN_LAYERS = [32, 32, 32, 32]
GRAIN_AMOUNT = 0.3
INPUT_DIR = "input"
OUTPUT_DIR = "output"

def initialize_network(layer_sizes, weight_range):
    weights = []
    biases = []
    all_layers = [3] + layer_sizes + [3]
    
    for i in range(len(all_layers) - 1):
        W = np.random.uniform(-weight_range, weight_range, (all_layers[i], all_layers[i+1]))
        b = np.random.uniform(-weight_range, weight_range, (all_layers[i+1],))
        weights.append(W)
        biases.append(b)
        
    return weights, biases

def forward_pass(data, weights, biases):
    current_activation = data
    
    for i in range(len(weights) - 1):
        net_input = np.dot(current_activation, weights[i]) + biases[i]
        current_activation = np.tanh(net_input)
        
    output = np.dot(current_activation, weights[-1]) + biases[-1]
    return np.tanh(output)

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

    weights, biases = initialize_network(HIDDEN_LAYERS, WEIGHT_INIT)

    print(f"Starting processing of {len(files)} frames using neural network...")
    print(f"Network architecture: 3 -> {' -> '.join(map(str, HIDDEN_LAYERS))} -> 3")

    for filename in files:
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        try:
            img = Image.open(input_path).convert('RGB')
            original_shape = np.array(img).shape
            
            data = np.array(img).astype(float) / 127.5 - 1.0
            flattened_data = data.reshape(-1, 3)

            processed_flat = forward_pass(flattened_data, weights, biases)
            saturated_data = processed_flat.reshape(original_shape)

            if GRAIN_AMOUNT > 0:
                noise = np.random.normal(0, GRAIN_AMOUNT * 0.2, saturated_data.shape)
                saturated_data += noise

            final_data = ((saturated_data + 1.0) * 127.5).clip(0, 255).astype(np.uint8)

            Image.fromarray(final_data).save(output_path)
            print(f"Done: {filename}")

        except Exception as e:
            print(f"Error processing file {filename}: {e}")

    print(f"\nProcessing completed! Output files are available in: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_sequence()
    input("\nPress Enter to exit...")