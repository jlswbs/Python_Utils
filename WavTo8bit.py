# Wav to 8bit table converter

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

# načtení jako float (soundfile vrací vždy float32 pokud nezadáš dtype)
data, samplerate = sf.read(input_wav)

if data.ndim > 1:
    data = data[:,0]

# normalizace do -1..+1 (pokud už je float, zůstane v rozsahu)
data = data.astype(np.float32)
data = data / np.max(np.abs(data))

# převod na int8 (-128..127)
data_int8 = (data * 127).astype(np.int8)

with open(output_h, "w") as f:
    f.write("const int SAMPLE_RATE = {};\n".format(samplerate))
    f.write("const int SAMPLE_COUNT = {};\n".format(len(data_int8)))
    f.write("const int8_t audio_table[SAMPLE_COUNT] = {\n")
    for i, sample in enumerate(data_int8):
        f.write("  {},".format(sample))
        if (i+1) % 16 == 0:
            f.write("\n")
    f.write("};\n")

print("Int8 header saved as", output_h)
