import os
import subprocess
import wave
import contextlib


def _audio_duration(path: str) -> float:
    with contextlib.closing(wave.open(path, "r")) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)


def _make_scene_clip(image_path: str, audio_path: str, out_path: str, vertical: bool = False):
    """One image, Ken Burns zoom/pan, duration = matching audio length, + narration audio."""
    duration = _audio_duration(audio_path)
    w, h = (1080, 1920) if vertical else (1920, 1080)
    fps = 30
    total_frames = max(int(duration * fps), fps)

    # slow zoom-in Ken Burns effect
    zoompan = (
        f"zoompan=z='min(zoom+0.0007,1.15)':d={total_frames}:s={w}x{h}:fps={fps}"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_path,
        "-i", audio_path,
        "-filter_complex", f"[0:v]scale={w*2}:{h*2},{zoompan}[v]",
        "-map", "[v]", "-map", "1:a",
        "-t", str(duration),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        out_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path


def assemble_video(image_paths: list, audio_paths: list, work_dir: str, out_path: str, vertical: bool = False) -> str:
    """Builds per-scene clips then concatenates them into the final video."""
    clips_dir = os.path.join(work_dir, "clips")
    os.makedirs(clips_dir, exist_ok=True)

    clip_paths = []
    for i, (img, aud) in enumerate(zip(image_paths, audio_paths)):
        clip_out = os.path.join(clips_dir, f"clip_{i:02d}.mp4")
        _make_scene_clip(img, aud, clip_out, vertical=vertical)
        clip_paths.append(clip_out)

    concat_list = os.path.join(work_dir, "concat.txt")
    with open(concat_list, "w") as f:
        for c in clip_paths:
            f.write(f"file '{os.path.abspath(c)}'\n")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c", "copy",
        out_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path


def make_thumbnail(image_path: str, out_path: str):
    """Just reuse the strongest scene image (scene 0) at 1280x720 as a fallback thumbnail."""
    cmd = ["ffmpeg", "-y", "-i", image_path, "-vf", "scale=1280:720", out_path]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path
