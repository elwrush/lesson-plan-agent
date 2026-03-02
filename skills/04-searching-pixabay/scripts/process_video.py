import argparse
import os
import subprocess
import sys

def process_video(input_path, output_path, max_duration=7, target_height=720):
    """
    Trims video to max_duration and scales to target_height (maintaining aspect ratio).
    Enforces strict file size limits.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        return False

    print(f"🎬 Processing video: {input_path}")
    print(f"   - Trim: {max_duration}s")
    print(f"   - Scale: {target_height}p")

    # FFmpeg command:
    # -y: Overwrite output
    # -i: Input
    # -t: Duration
    # -vf: Scale filter (width=-2 maintains aspect ratio and ensures divisibility by 2)
    # -c:v libx264: Encoder
    # -crf 26: Quality (lower is better, 23 is default, 28 is compressed)
    # -preset fast: Encoding speed
    # -an: Remove audio (save space)
    
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-t", str(max_duration),
        "-vf", f"scale=-2:{target_height}",
        "-c:v", "libx264",
        "-crf", "26",
        "-preset", "medium",
        "-an",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg failed: {e}")
        return False

    # Validation
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✅ Processed. New Size: {size_mb:.2f} MB")

    if size_mb > 10:
        print("⚠️ WARNING: Video is still > 10MB. Consider lowering resolution.")
        return False
    
    # Automated Cleanup of Monster File
    try:
        os.remove(input_path)
        print(f"🗑️ Cleaned up raw file: {input_path}")
    except OSError as e:
        print(f"⚠️ Failed to delete raw file: {e}")

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trim and compress video for slide background.")
    parser.add_argument("input", help="Path to raw video")
    parser.add_argument("output", help="Path to output video")
    
    args = parser.parse_args()
    
    success = process_video(args.input, args.output)
    if not success:
        sys.exit(1)
