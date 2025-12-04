# Midi Type1 to Type0 converter

import sys
import argparse
import os
from mido import MidiFile, MidiTrack, MetaMessage

def convert_type1_to_type0(input_path: str, overwrite_if_type0: bool=False):
    mid = MidiFile(input_path)
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_type0.mid"

    if mid.type == 0 and not overwrite_if_type0:
        mid.save(output_path)
        return output_path

    ticks_per_beat = mid.ticks_per_beat
    events = []

    for ti, track in enumerate(mid.tracks):
        abs_time = 0
        for msg in track:
            abs_time += msg.time
            try:
                msg_copy = msg.copy()
            except Exception:
                msg_copy = msg
            events.append((abs_time, ti, msg_copy))

    events.sort(key=lambda e: (e[0], e[1]))

    out_mid = MidiFile(type=0)
    out_mid.ticks_per_beat = ticks_per_beat
    out_track = MidiTrack()
    out_mid.tracks.append(out_track)

    prev_time = 0
    for abs_time, ti, msg in events:
        delta = abs_time - prev_time
        new_msg = msg.copy()
        new_msg.time = delta
        out_track.append(new_msg)
        prev_time = abs_time

    if not (len(out_track) and isinstance(out_track[-1], MetaMessage) and out_track[-1].type == 'end_of_track'):
        out_track.append(MetaMessage('end_of_track', time=0))

    out_mid.save(output_path)
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Convert MIDI type 1 files to type 0 (single track).")
    parser.add_argument("input", help="Input MIDI file (type 1)")
    parser.add_argument("--force", "-f", action="store_true", help="If input is already type 0, still rewrite output")
    args = parser.parse_args()

    try:
        output_file = convert_type1_to_type0(args.input, overwrite_if_type0=args.force)
        print(f"Done: {args.input} -> {output_file}")
    except Exception as e:
        print("Error during conversion:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()