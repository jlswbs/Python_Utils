# Wav to float wavetable converter (resampled to fixed size)

import numpy as np
import soundfile as sf
import os
import sys

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

# normalizace
data = data / np.max(np.abs(data))

# přepočet na pevnou délku tabulky
x_old = np.linspace(0, 1, len(data))
x_new = np.linspace(0, 1, table_size)
wavetable = np.interp(x_new, x_old, data)

# uložení do headeru
base_name = os.path.splitext(os.path.basename(wav_file))[0]
header_file = base_name + ".h"

with open(header_file, "w") as f:
    f.write(f"#pragma once\n\n")
    f.write(f"const int TABLE_SIZE = {table_size};\n")
    f.write("const float wavetable[TABLE_SIZE] = {\n")
    for i, val in enumerate(wavetable):
        f.write(f"  {val:.6f}f")
        if i < table_size - 1:
            f.write(",")
        if (i+1) % 8 == 0:
            f.write("\n")
    f.write("};\n")

print(f"Header saved as: {header_file}")
