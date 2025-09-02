'''
Test that we can stream a basic Windows 11 screen into appropriate WebM chunks for the chain.
'''

import subprocess
import os

def record_chunks():
    cmd = [
        "ffmpeg",
        "-f", "gdigrab",
        "-framerate", "30",
        "-i", "desktop",
        "-r", "30",                        # enforce 30 fps output
        "-vf", "format=yuv420p,scale=1920:1080",          # downscale (optional)
        "-c:v", "libvpx",                  # VP8 faster than VP9
        "-deadline", "realtime",
        "-cpu-used", "8",
        "-b:v", "2M",
        "-f", "segment",
        "-segment_time", "2",
        "-reset_timestamps", "1",
        "-segment_format", "webm",
        "chunks/chunk%03d.webm"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":

    for f in os.listdir("chunks/"):
        file_path = os.path.join("chunks/", f)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. {e}")

    record_chunks()
