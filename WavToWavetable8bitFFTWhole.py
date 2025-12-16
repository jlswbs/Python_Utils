# Wav to uint8_t wavetable converter (FFT resampled to fixed size)

import numpy as np
import soundfile as sf
import os
import sys
from scipy.signal import resample

if len(sys.argv) < 2:
    print("Usage: python script.py input.wav [table_size]")
    sys.exit(1)

wav_file = sys.argv[1]
table_size = int(sys.argv[2]) if len(sys.argv) > 2 else 1024

# načtení wav
data, samplerate = sf.read(wav_file)

# mono
if data.ndim > 1:
    data = data[:,0]

# normalizace do [-1,1]
data = data / np.max(np.abs(data))

# FFT resampling na pevnou délku
wavetable = resample(data, table_size)

# mapování [-1,1] -> [0,255]
wavetable_uint8 = ((wavetable + 1.0) * 127.5).astype(np.uint8)

# uložení do headeru
base_name = os.path.splitext(os.path.basename(wav_file))[0]
header_file = base_name + ".h"

with open(header_file, "w") as f:
    f.write(f"#pragma once\n\n")
    f.write(f"const int TABLE_SIZE = {table_size};\n")
    f.write("const uint8_t wavetable[TABLE_SIZE] = {\n")
    for i, val in enumerate(wavetable_uint8):
        f.write(f"  {val}")
        if i < table_size - 1:
            f.write(",")
        if (i+1) % 16 == 0:  # víc hodnot na řádek, protože jsou malé
            f.write("\n")
    f.write("};\n")

print(f"Header saved as: {header_file}")