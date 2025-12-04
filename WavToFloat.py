# Wav to float table converter

import sys
import os
import numpy as np
import soundfile as sf

if len(sys.argv) < 2:
    print("Usage: python script.py <input.wav>")
    sys.exit(1)

input_wav = sys.argv[1]
base_name = os.path.splitext(os.path.basename(input_wav))[0]
output_h = base_name + ".h"

data, samplerate = sf.read(input_wav)

if data.ndim > 1:
    data = data[:,0]

data = data.astype(np.float32)
data = data / np.max(np.abs(data))

with open(output_h, "w") as f:
    f.write("const int SAMPLE_RATE = {};\n".format(samplerate))
    f.write("const int SAMPLE_COUNT = {};\n".format(len(data)))
    f.write("const float audio_table[SAMPLE_COUNT] = {\n")
    for i, sample in enumerate(data):
        f.write("  {:.6f},".format(sample))
        if (i+1) % 8 == 0:
            f.write("\n")
    f.write("};\n")

print("Header saved as", output_h)