# Wav to int8_t FFT table converter (FFT resampled to fixed size)

import numpy as np
import soundfile as sf
from scipy import signal
import os
import sys

if len(sys.argv) < 2:
    sys.exit(1)

wav_file = sys.argv[1]
table_size = int(sys.argv[2]) if len(sys.argv) > 2 else 2048

data, samplerate = sf.read(wav_file)

if data.ndim > 1:
    data = data[:, 0]

# Tady probíhá "stlačení" celého WAVu do table_size
if len(data) != table_size:
    data = signal.resample(data, table_size)

fft_data = np.fft.fft(data)
real_part = fft_data.real
imag_part = fft_data.imag

def to_int8(arr):
    abs_max = max(np.max(np.abs(real_part)), np.max(np.abs(imag_part)))
    if abs_max == 0: 
        return np.zeros_like(arr, dtype=np.int8)
    normalized = (arr / abs_max) * 127.0
    return normalized.astype(np.int8)

real_int8 = to_int8(real_part)
imag_int8 = to_int8(imag_part)

header_file = "table.h"

with open(header_file, "w") as f:
    f.write(f"#pragma once\n#include <stdint.h>\n\n")
    f.write(f"const uint16_t wavetable_size = {table_size};\n\n")
    
    for name, data_array in [("wavetable_real", real_int8), ("wavetable_imag", imag_int8)]:
        f.write(f"const int8_t {name}[{table_size}] = {{\n  ")
        for i, val in enumerate(data_array):
            f.write(f"{val:4}")
            if i < table_size - 1:
                f.write(",")
            if (i+1) % 16 == 0:
                f.write("\n  ")
            else:
                f.write(" ")
        f.write("\n};\n\n")

print(f"Hotovo: {header_file}")
