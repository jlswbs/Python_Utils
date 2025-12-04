# Wav to float FFT wavetable converter

import numpy as np
import soundfile as sf
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python script.py input.wav")
    sys.exit(1)

wav_file = sys.argv[1]
data, samplerate = sf.read(wav_file)

if data.ndim > 1:
    data = data[:,0]

data = data / np.max(np.abs(data))

N = 2048
segment = data[:N]
spectrum = np.fft.fft(segment)
magnitudes = np.abs(spectrum)

harmonics = magnitudes[:N//2]
harmonics = harmonics / np.max(harmonics)

wavetable = np.fft.ifft(harmonics).real
wavetable = wavetable / np.max(np.abs(wavetable))

table_size = len(wavetable)
base_name = os.path.splitext(os.path.basename(wav_file))[0]
header_file = base_name + ".h"

with open(header_file, "w") as f:
    f.write("#pragma once\n\n")
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
