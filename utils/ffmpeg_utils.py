import subprocess

def video_to_gif(input_path: str, output_path: str, fps: int = 10, width: int = 480):
    """
    Convert a video file to a GIF using ffmpeg.
    """

    # Create GIF command
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", f"fps={fps},scale={width}:-1:flags=lanczos",
        "-loop", "0",
        output_path
    ]

    # Run the command
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return output_path
