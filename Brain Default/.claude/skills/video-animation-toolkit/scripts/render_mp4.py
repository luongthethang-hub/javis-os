"""Render and verify a local MP4 from an explicit edit plan."""

import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from uuid import uuid4


VAULT = Path(__file__).resolve().parents[3]
SIZES = {"9:16": (720, 1280), "16:9": (1280, 720), "1:1": (720, 720)}
FPS = 30


def binary(name):
    found = shutil.which(os.getenv(f"JAVIS_{name.upper()}") or name)
    if found:
        return found
    local = os.getenv("LOCALAPPDATA")
    if os.name == "nt" and local:
        packages = Path(local) / "Microsoft" / "WinGet" / "Packages"
        for path in packages.glob(f"Gyan.FFmpeg*/*/bin/{name}.exe"):
            if path.is_file():
                return str(path)
    raise ValueError(f"Không tìm thấy {name}.")


def run(tool, *args, timeout=20, cwd=None):
    result = subprocess.run(
        [tool, *map(str, args)], stdin=subprocess.DEVNULL, capture_output=True,
        encoding="utf-8", errors="replace", timeout=timeout, cwd=cwd,
    )
    if result.returncode:
        raise ValueError(f"{Path(tool).name} (mã {result.returncode}): {result.stderr.strip()[-2000:]}")
    return result.stdout


def vault_file(name, suffixes):
    path = (VAULT / name).resolve(strict=True)
    if not path.is_relative_to(VAULT) or not path.is_file() or path.suffix.lower() not in suffixes:
        raise ValueError(f"Đường dẫn tệp trong brain không hợp lệ: {name}")
    return path


def probe(tool, path):
    data = json.loads(run(tool, "-v", "error", "-protocol_whitelist", "file", "-f", "mov",
                          "-show_streams", "-show_format", "-of", "json", path))
    streams = data["streams"]
    video = next((s for s in streams if s["codec_type"] == "video"
                  and not s.get("disposition", {}).get("attached_pic")), None)
    audio = next((s for s in streams if s["codec_type"] == "audio"), None)
    if video is None:
        raise ValueError(f"Không có luồng hình trong {path.name}.")
    duration = float(video.get("duration") or data["format"]["duration"])
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError(f"Không đọc được thời lượng {path.name}.")
    return duration, video, audio


def render(plan_path):
    plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))
    if not isinstance(plan, dict) or set(plan) - {"clips", "ratio", "fit", "audio", "subtitles"}:
        raise ValueError("Kế hoạch dựng không hợp lệ.")
    ratio, fit, sound = (plan.get("ratio", "9:16"), plan.get("fit", "pad"), plan.get("audio", "keep"))
    if ratio not in SIZES or fit not in ("pad", "crop") or sound not in ("keep", "mute"):
        raise ValueError("Tỷ lệ, kiểu giữ khung hoặc âm thanh không hợp lệ.")
    clips = plan.get("clips")
    if not isinstance(clips, list) or not 1 <= len(clips) <= 20:
        raise ValueError("Cần từ 1 đến 20 đoạn clip.")

    ffmpeg, ffprobe = binary("ffmpeg"), binary("ffprobe")
    w, h = SIZES[ratio]
    geometry = (f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}" if fit == "crop"
                else f"scale={w}:{h}:force_original_aspect_ratio=decrease:force_divisible_by=2,"
                     f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2")
    inputs, filters, labels = [], [], []
    total = 0.0
    for i, clip in enumerate(clips):
        if not isinstance(clip, dict) or set(clip) - {"path", "start", "end"}:
            raise ValueError(f"Đoạn {i + 1} không hợp lệ.")
        source = vault_file(clip["path"], {".mp4", ".mov"})
        duration, video, audio = probe(ffprobe, source)
        start, end = clip.get("start", 0), clip.get("end", duration)
        if any(type(t) not in (int, float) or not math.isfinite(t) for t in (start, end)):
            raise ValueError(f"Mốc cắt của {source.name} phải là số giây.")
        if not 0 <= start < end <= duration + 0.05 or min(end, duration) - start < 2 / FPS:
            raise ValueError(f"Mốc cắt của {source.name} nằm ngoài đoạn khả dụng ({duration:.3f} giây).")
        length = min(end, duration) - start
        total += length
        inputs.extend(("-ss", f"{start:.6f}", "-t", f"{length:.6f}",
                       "-protocol_whitelist", "file", "-f", "mov", "-i", source))
        filters.append(f"[{i}:{video['index']}]{geometry},setsar=1,fps={FPS},format=yuv420p,"
                       f"setpts=PTS-STARTPTS[v{i}]")
        labels.append(f"[v{i}]")
        if sound == "keep":
            audio_filter = (f"[{i}:{audio['index']}]aresample=48000,apad" if audio
                            else "anullsrc=r=48000:cl=stereo")
            filters.append(f"{audio_filter},aformat=sample_fmts=fltp:channel_layouts=stereo,"
                           f"atrim=duration={length:.6f},asetpts=PTS-STARTPTS[a{i}]")
            labels.append(f"[a{i}]")
    if total > 180:
        raise ValueError("Bản dựng tối đa 180 giây.")

    subtitles = vault_file(plan["subtitles"], {".srt"}) if plan.get("subtitles") else None
    has_audio = sound == "keep"
    filters.append(f"{''.join(labels)}concat=n={len(clips)}:v=1:a={int(has_audio)}"
                   f"{'[joined]' if subtitles else '[outv]'}{'[outa]' if has_audio else ''}")
    if subtitles:
        filters.append("[joined]subtitles=filename=captions.srt:charenc=UTF-8[outv]")

    output_dir = (VAULT / "attachments" / "video-production").resolve()
    if not output_dir.is_relative_to(VAULT):
        raise ValueError("Thư mục xuất phải nằm trong brain.")
    output_dir.mkdir(parents=True, exist_ok=True)
    final = output_dir / f"javis-video-{uuid4().hex}.mp4"
    with TemporaryDirectory(dir=output_dir) as stage:
        if subtitles:
            shutil.copyfile(subtitles, Path(stage) / "captions.srt")
        staged = Path(stage) / "video.mp4"
        audio_args = ["-map", "[outa]", "-c:a", "aac", "-b:a", "128k"] if has_audio else ["-an"]
        run(ffmpeg, "-nostdin", "-v", "error", "-xerror", *inputs, "-filter_complex_threads", "2",
            "-filter_complex", ";".join(filters), "-map", "[outv]", *audio_args,
            "-c:v", "libx264", "-threads", "4", "-preset", "fast", "-crf", "22",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", staged, timeout=240, cwd=stage)
        actual, video, audio = probe(ffprobe, staged)
        if (abs(total - actual) > max(0.2, len(clips) / FPS) or video["codec_name"] != "h264"
                or (video["width"], video["height"]) != (w, h) or video["avg_frame_rate"] != "30/1"
                or bool(audio) != has_audio or (audio and audio["codec_name"] != "aac")):
            raise ValueError("MP4 không đạt thời lượng, khung hình, tốc độ khung hình hoặc âm thanh.")
        run(ffmpeg, "-nostdin", "-v", "error", "-xerror", "-protocol_whitelist", "file",
            "-i", staged, "-map", "0:v:0", "-map", "0:a:0?", "-f", "null", "-", timeout=120)
        with staged.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        size = staged.stat().st_size
        staged.replace(final)
    return {"path": final.relative_to(VAULT).as_posix(), "seconds": round(actual, 3), "width": w,
            "height": h, "fps": FPS, "audio": "aac" if has_audio else None, "bytes": size, "sha256": digest}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Dùng: python render_mp4.py <kế-hoạch.json>")
    try:
        print(json.dumps(render(vault_file(sys.argv[1], {".json"})), ensure_ascii=True))
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        sys.exit(str(exc))
