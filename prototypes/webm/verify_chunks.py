import subprocess
import json
import os

def validate_webm(path, min_size=100_000, max_size=10_000_000,
                  target_fps=30, tol=1, min_length=1, max_length=5):
    # check file exists
    if not os.path.isfile(path):
        return False, "File not found"

    # check extension
    if not path.lower().endswith(".webm"):
        return False, "Not a .webm file"

    # check size
    fsize = os.path.getsize(path)
    if fsize < min_size or fsize > max_size:
        return False, f"File size {fsize} outside allowed range"

    # run ffprobe
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size:stream=avg_frame_rate",
        "-of", "json", path
    ]
    try:
        output = subprocess.check_output(cmd, text=True)
        info = json.loads(output)
    except subprocess.CalledProcessError:
        return False, "Invalid WebM (ffprobe failed)"

    # duration
    duration = float(info["format"]["duration"])
    if not (min_length <= duration <= max_length):
        return False, f"Duration {duration:.2f}s outside allowed range"

    # framerate
    fps_str = info["streams"][0].get("avg_frame_rate", "0/1")
    num, den = fps_str.split("/")
    fps = float(num) / float(den) if float(den) != 0 else 0
    if not (target_fps - tol <= fps <= target_fps + tol):
        return False, f"FPS {fps:.2f} not near {target_fps}"

    return True, "Valid WebM"

ok, msg = validate_webm("chunks/chunk002.webm",
                        min_size=50_000, max_size=5_000_000,
                        target_fps=30, tol=2,
                        min_length=1, max_length=7)
print(ok, msg)