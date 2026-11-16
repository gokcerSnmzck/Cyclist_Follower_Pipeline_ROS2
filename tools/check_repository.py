#!/usr/bin/env python3
"""Read-only syntax/manifest/startup checks. Does not import nodes or start ROS."""

import ast
from collections import defaultdict
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    counts = defaultdict(int)
    packages = defaultdict(list)
    for directory in ("src", "CAN_Combined_Pipeline/src", "tests", "tools"):
        for path in sorted((ROOT / directory).rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            counts["python"] += 1
            try:
                ast.parse(path.read_text(), filename=str(path.relative_to(ROOT)))
            except SyntaxError as exc:
                errors.append(f"{path.relative_to(ROOT)}:{exc.lineno}: {exc.msg}")
    for directory in ("src", "CAN_Combined_Pipeline/src"):
        for path in sorted((ROOT / directory).rglob("package.xml")):
            counts["manifests"] += 1
            try:
                manifest = ET.parse(path)
                name = manifest.findtext("name")
                if not name:
                    errors.append(f"{path.relative_to(ROOT)}: missing package name")
                packages[name].append(str(path.parent.relative_to(ROOT)))
            except ET.ParseError as exc:
                errors.append(f"{path.relative_to(ROOT)}: {exc}")
    for directory in ("startup_scripts", "CAN_Combined_Pipeline/startup_scripts"):
        for path in sorted((ROOT / directory).glob("*.sh")):
            counts["shell"] += 1
            result = subprocess.run(["bash", "-n", str(path)],
                                    capture_output=True, text=True, check=False)
            if result.returncode:
                errors.append(result.stderr.strip().replace(str(ROOT) + "/", ""))
    print(f"Checked {counts['python']} Python files, {counts['manifests']} XML "
          f"manifests, {counts['shell']} shell scripts (syntax only).")
    duplicate_names = [name for name, paths in packages.items() if len(paths) > 1]
    print("Separate workspace builds required; duplicate names: " +
          ", ".join(sorted(duplicate_names)))
    if not (ROOT / ".gitmodules").exists():
        print("BLOCKER: ZED gitlinks have no .gitmodules URL mapping; see docs/INSTALLATION.md.")
    for error in errors:
        print("ERROR:", error)
    print(f"{len(errors)} syntax/manifest error(s). Runtime dependencies and hardware not tested.")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
