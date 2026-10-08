#!/usr/bin/env python3
"""Split a self-contained script into editable files, and join them back.

  tools/assets.py split <script> <dir>   head.sh, every asset as a file, order.txt
  tools/assets.py join <dir> <script>    rebuild the script, then check every asset
                                         extracts byte-identical with the script's own awk
A new asset is added by creating its file and listing it in order.txt.
"""
import os, subprocess, sys
from pathlib import Path

START, END = "#=== ASSET {} ===", "#=== END ==="


def split(script, out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    lines = Path(script).read_text().split("\n")
    first = next(i for i, l in enumerate(lines) if l.startswith("#=== ASSET ") and l.endswith(" ==="))
    (out / "head.sh").write_text("\n".join(lines[:first]) + "\n")   # code, exit, and the gap before the assets
    order, i = [], first
    while i < len(lines):
        line = lines[i]
        if line.startswith("#=== ASSET ") and line.endswith(" ==="):
            name = line[len("#=== ASSET "):-len(" ===")]
            j = lines.index(END, i + 1)
            path = out / "assets" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("\n".join(lines[i + 1:j]) + "\n")
            order.append(name)
            i = j + 1
        else:
            i += 1
    (out / "order.txt").write_text("\n".join(order) + "\n")
    print(f"split {len(order)} assets into {out}")


def join(src, script):
    src = Path(src)
    order = [n for n in (src / "order.txt").read_text().split("\n") if n]
    parts = [(src / "head.sh").read_text()[:-1]]
    for name in order:
        body = (src / "assets" / name).read_text()
        if not body.endswith("\n"):
            raise SystemExit(f"{name}: must end with a newline")
        if any(l == END or (l.startswith("#=== ASSET ") and l.endswith(" ===")) for l in body.split("\n")):
            raise SystemExit(f"{name}: contains a marker line")
        parts.append(START.format(name) + "\n" + body.rstrip("\n") + "\n" + END)
    tmp = Path(str(script) + ".new")
    tmp.write_text("\n".join(parts) + "\n")
    os.chmod(tmp, 0o755)
    for name in order:
        got = subprocess.run(["awk", '$0 == start {on=1; next} on && $0 == "#=== END ===" {exit} on',
                              "start=" + START.format(name), str(tmp)], capture_output=True, text=True).stdout
        if got != (src / "assets" / name).read_text():
            tmp.unlink()
            raise SystemExit(f"{name}: does not extract byte-identical")
    code = (src / "head.sh").read_text().split("\nexit\n")[0] + "\nexit\n"
    head = subprocess.run(["sh", "-n"], input=code, capture_output=True, text=True)
    if head.returncode:
        tmp.unlink()
        raise SystemExit("shell part: " + head.stderr)
    tmp.replace(script)
    print(f"joined {len(order)} assets into {script}; all extract byte-identical")


if __name__ == "__main__":
    {"split": split, "join": join}[sys.argv[1]](sys.argv[2], sys.argv[3])
