#!/usr/bin/env python3
"""Describe historical log-event rates; deliberately makes no latency estimate."""

import argparse
from decimal import Decimal
from pathlib import Path
import re
import statistics

ROOT = Path(__file__).resolve().parents[1]
EVENTS = {"follower.log": "Following person ID", "fusion.log": "Published target ID",
          "cmdvel_to_can.log": "Published CtrlCmd:"}


def summarize(path, marker):
    timestamps = []
    for line in path.read_text().splitlines():
        if marker in line:
            match = re.search(r"\[(\d+\.\d+)\]", line)
            if match:
                timestamps.append(Decimal(match[1]))
    if len(timestamps) < 2:
        raise ValueError(f"{path}: fewer than two matching timestamped events")
    intervals = [b - a for a, b in zip(timestamps, timestamps[1:])]
    if any(dt <= 0 for dt in intervals):
        raise ValueError(f"{path}: timestamps are not strictly increasing")
    span = timestamps[-1] - timestamps[0]
    rate = Decimal(len(intervals)) / span
    return (f"{path.name}: events={len(timestamps)}, span={span:.6f} s, "
            f"rate={rate:.3f} events/s, median_interval={statistics.median(intervals)*1000:.3f} ms")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-dir", type=Path,
                        default=ROOT / "CAN_Combined_Pipeline/startup_scripts")
    args = parser.parse_args()
    for filename, marker in EVENTS.items():
        print(summarize(args.log_dir / filename, marker))
    print("Rates describe logged events between first and last match; not camera/inference FPS.")
    print("No shared frame ID/acquisition timestamp: cross-file subtraction is not end-to-end latency.")


if __name__ == "__main__":
    main()
