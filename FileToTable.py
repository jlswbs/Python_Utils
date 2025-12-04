# File to table converter

import sys
import os

if len(sys.argv) < 2:
    print("Usage: python script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
base_name = os.path.splitext(os.path.basename(input_file))[0]
output_h = base_name + ".h"

with open(input_file, "rb") as f:
    data = f.read()

with open(output_h, "w") as f:
    f.write("const int FILE_SIZE = {};\n".format(len(data)))
    f.write("const unsigned char file_data[FILE_SIZE] = {\n")
    for i, byte in enumerate(data):
        f.write("  {},".format(byte))
        if (i+1) % 16 == 0:
            f.write("\n")
    f.write("};\n")

print("Raw 8-bit header saved as", output_h)