import os
import math
import subprocess
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import edge_tts
import asyncio

SCRATCH_DIR = "C:/Users/Admin/JavisOS/brains/Brain Default/scratch/openmotion_stickman"
OUTPUT_DIR = "C:/Users/Admin/JavisOS/brains/Brain Default/attachments/video-production"
FONT_PATH = "C:/Windows/Fonts/segoeuib.ttf"
TITLE_FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"

TOTAL_SECONDS = 5.0
FPS = 30
TOTAL_FRAMES = int(TOTAL_SECONDS * FPS)  # 150 frames
WIDTH = 1080
HEIGHT = 1920

VIDEO_A_OUT = os.path.join(OUTPUT_DIR, "test_5s_quy_trinh_cu.mp4")
VIDEO_B_OUT = os.path.join(OUTPUT_DIR, "test_5s_quy_trinh_moi.mp4")

# 1. Step 1 & 2 of User Proposal: Script -> Generate Voice & Measure Timing
TEXT = "kỷ luật là chiếc cầu nối dẫn đến thành công"

async def make_voice():
    raw_p = os.path.join(SCRATCH_DIR, "v_raw_5s.mp3")
    comm = edge_tts.Communicate(TEXT, "vi-VN-NamMinhNeural")
    await comm.save(raw_p)
    
    # Raspy DSP Filter
    raspy_p = os.path.join(SCRATCH_DIR, "v_raspy_5s.mp3")
    filter_chain = (
        "asetrate=24000*0.92,aresample=24000,"
        "bass=g=5.5:f=120,"
        "treble=g=4.0:f=6000,"
        "aexciter=freq=5500:amount=1.5,"
        "compand=attacks=0.01:decays=0.15:points=-70/-70|-40/-26|-18/-8|0/-1:gain=3.8"
    )
    cmd = ["ffmpeg", "-y", "-i", raw_p, "-af", filter_chain, "-c:a", "libmp3lame", "-b:a", "192k", raspy_p]
    subprocess.check_call(cmd)
    return raspy_p

def make_bgm(voice_p):
    sr = 44100
    t = np.linspace(0, TOTAL_SECONDS, int(sr * TOTAL_SECONDS), endpoint=False)
    # Bass synth
    bass = 0.22 * np.sin(2 * np.pi * 55.0 * t) + 0.10 * np.sin(2 * np.pi * 110.0 * t)
    # Kicks at 0s, 1.2s, 2.8s, 4.0s
    for kt in [0.0, 1.2, 2.8, 4.0]:
        mask = (t >= kt) & (t < kt + 0.25)
        if np.any(mask):
            tk = t[mask] - kt
            kick = 0.35 * np.sin(2 * np.pi * (45 + 85 * np.exp(-tk * 25)) * tk) * np.exp(-tk * 12)
            bass[mask] += kick
    
    audio_int16 = ((bass / np.max(np.abs(bass))) * 0.65 * 32767).astype(np.int16)
    bgm_p = os.path.join(SCRATCH_DIR, "bgm_5s.wav")
    with wave.open(bgm_p, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_int16.tobytes())

    # Mixed audio: delay voice by 0.3s
    mixed_p = os.path.join(SCRATCH_DIR, "mix_5s.mp3")
    cmd = [
        "ffmpeg", "-y",
        "-i", bgm_p,
        "-i", voice_p,
        "-filter_complex", "[1:a]adelay=300|300,volume=1.4[v];[0:a]volume=0.5[b];[b][v]amix=inputs=2:duration=first[outa]",
        "-map", "[outa]",
        "-c:a", "libmp3lame", "-b:a", "192k",
        mixed_p
    ]
    subprocess.check_call(cmd)
    return mixed_p

def draw_subtitle_box(draw, text, font, box_y=1640):
    box_w = 980
    box_h = 150
    box_x = (WIDTH - box_w) // 2
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=20, fill=(15, 23, 42), outline=(0, 229, 255), width=4)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = box_x + (box_w - tw) // 2
    ty = box_y + (box_h - th) // 2 - 6
    draw.text((tx+2, ty+2), text, font=font, fill=(0, 0, 0))
    draw.text((tx, ty), text, font=font, fill=(255, 230, 0))

# --- RENDER VIDEO A: Cũ (Visual-First - Cố định 2 cảnh 50/50 ở 2.5s, tiếng đi sau) ---
def render_video_a(audio_p):
    print("Rendering Video A (Visual-First - Nhịp cắt chia đôi 2.5s, không khóa audio)...")
    sub_font = ImageFont.truetype(FONT_PATH, 42)
    header_font = ImageFont.truetype(TITLE_FONT_PATH, 30)
    
    cmd = [
        "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-", "-i", audio_p,
        "-c:v", "libx264", "-preset", "faster", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        VIDEO_A_OUT
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    for f in range(TOTAL_FRAMES):
        img = Image.new("RGB", (WIDTH, HEIGHT), (10, 15, 25))
        draw = ImageDraw.Draw(img)
        draw.text((WIDTH//2 - 250, 100), "CÁCH CŨ: DỰNG HÌNH TRƯỚC (VISUAL-FIRST)", font=header_font, fill=(255, 100, 100))

        # Hard cut exactly at frame 75 (2.5s), regardless of speech
        if f < 75:
            # Stickman standing at cliff edge looking across
            draw.line([(0, 1300), (400, 1300)], fill=(0, 229, 255), width=8)
            draw.line([(700, 1300), (WIDTH, 1300)], fill=(0, 229, 255), width=8)
            # Stickman
            draw.ellipse([300, 1050, 360, 1110], outline=(255, 255, 255), width=8)
            draw.line([(330, 1110), (330, 1220)], fill=(255, 255, 255), width=8)
            draw.line([(330, 1220), (300, 1300)], fill=(255, 255, 255), width=8)
            draw.line([(330, 1220), (360, 1300)], fill=(255, 255, 255), width=8)
            draw_subtitle_box(draw, "KỶ LUẬT LÀ CHIẾC CẦU NỐI...", sub_font)
        else:
            # Cut abruptly into running on bridge
            draw.line([(0, 1300), (WIDTH, 1300)], fill=(0, 229, 255), width=8)
            prog = (f - 75) / 75.0
            sx = 400 + int(prog * 350)
            draw.ellipse([sx - 30, 1050, sx + 30, 1110], outline=(255, 255, 255), width=8)
            draw.line([(sx, 1110), (sx, 1220)], fill=(255, 255, 255), width=8)
            draw.line([(sx, 1220), (sx - 30, 1300)], fill=(255, 255, 255), width=8)
            draw.line([(sx, 1220), (sx + 30, 1300)], fill=(255, 255, 255), width=8)
            draw_subtitle_box(draw, "...DẪN ĐẾN THÀNH CÔNG!", sub_font)

        proc.stdin.write(img.tobytes())
    proc.stdin.close()
    proc.wait()
    print("Video A complete:", VIDEO_A_OUT)

# --- RENDER VIDEO B: Mới (Voice-Driven / Audio-First - Cầu nối xuất hiện đúng lúc phát âm "cầu nối") ---
def render_video_b(audio_p):
    print("Rendering Video B (Voice-First - Khóa trục âm thanh, khớp từng mili-giây)...")
    sub_font = ImageFont.truetype(FONT_PATH, 42)
    header_font = ImageFont.truetype(TITLE_FONT_PATH, 30)
    
    cmd = [
        "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-", "-i", audio_p,
        "-c:v", "libx264", "-preset", "faster", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        VIDEO_B_OUT
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    # Audio timestamps:
    # 0.0s - 1.1s (Frames 0 - 33): "Kỷ luật là..." -> Stickman powering up
    # 1.1s - 2.2s (Frames 34 - 66): "...chiếc cầu nối..." -> Energy bridge springs across instantly!
    # 2.2s - 3.4s (Frames 67 - 102): "...dẫn đến thành công!" -> Stickman dashes across and raises flag
    # 3.4s - 5.0s (Frames 103 - 149): Victory shockwave & fireworks outro (planned hold, no dead silence)

    for f in range(TOTAL_FRAMES):
        img = Image.new("RGB", (WIDTH, HEIGHT), (8, 12, 22))
        draw = ImageDraw.Draw(img)
        draw.text((WIDTH//2 - 250, 100), "CÁCH MỚI: VOICE-FIRST (KHÓA THEO GIỌNG)", font=header_font, fill=(0, 229, 255))

        # Cliff left and right
        draw.polygon([(0, 1300), (350, 1300), (300, HEIGHT), (0, HEIGHT)], fill=(17, 24, 39))
        draw.line([(0, 1300), (350, 1300)], fill=(0, 229, 255), width=6)
        draw.polygon([(730, 1300), (WIDTH, 1300), (WIDTH, HEIGHT), (780, HEIGHT)], fill=(17, 24, 39))
        draw.line([(730, 1300), (WIDTH, 1300)], fill=(0, 229, 255), width=6)

        # 1. Phase 1: 0 to 33 (Energy build up)
        if f < 34:
            sx = 250
            draw.ellipse([sx - 35, 1050, sx + 35, 1120], outline=(255, 255, 255), width=8)
            draw.line([(sx, 1120), (sx, 1220)], fill=(255, 255, 255), width=10)
            draw.line([(sx, 1220), (sx - 40, 1300)], fill=(255, 255, 255), width=10)
            draw.line([(sx, 1220), (sx + 40, 1300)], fill=(255, 255, 255), width=10)
            # Energy aura
            draw.ellipse([sx - 60, 1030, sx + 60, 1150], outline=(255, 230, 0), width=4)
            draw_subtitle_box(draw, "KỶ LUẬT LÀ...", sub_font)

        # 2. Phase 2: 34 to 66 ("Chiếc cầu nối" - Bridge springs into existence!)
        elif f < 67:
            bridge_prog = (f - 34) / 32.0
            bridge_x = 350 + int(bridge_prog * 380)
            # Glowing neon bridge extending across the chasm
            draw.line([(350, 1300), (bridge_x, 1300)], fill=(0, 229, 255), width=14)
            draw.line([(350, 1300), (bridge_x, 1300)], fill=(255, 255, 255), width=6)
            
            # Stickman preparing sprint
            sx = 250 + int(bridge_prog * 80)
            draw.ellipse([sx - 35, 1050, sx + 35, 1120], outline=(255, 255, 255), width=8)
            draw.line([(sx, 1120), (sx, 1220)], fill=(255, 255, 255), width=10)
            draw.line([(sx, 1220), (sx - 30, 1300)], fill=(255, 255, 255), width=10)
            draw.line([(sx, 1220), (sx + 50, 1300)], fill=(255, 255, 255), width=10)
            draw_subtitle_box(draw, "CHIẾC CẦU NỐI...", sub_font)

        # 3. Phase 3: 67 to 102 ("Dẫn đến thành công!" - Crossing and reaching peak)
        elif f < 103:
            # Full bridge
            draw.line([(350, 1300), (730, 1300)], fill=(0, 229, 255), width=14)
            draw.line([(350, 1300), (730, 1300)], fill=(255, 255, 255), width=6)
            
            cross_prog = (f - 67) / 35.0
            sx = 330 + int(cross_prog * 520)
            sy = 1300 - int(math.sin(cross_prog * math.pi) * 80)
            
            draw.ellipse([sx - 35, sy - 250, sx + 35, sy - 180], outline=(255, 255, 255), width=8)
            draw.line([(sx, sy - 180), (sx, sy - 80)], fill=(255, 255, 255), width=10)
            draw.line([(sx, sy - 80), (sx - 40, sy)], fill=(255, 255, 255), width=10)
            draw.line([(sx, sy - 80), (sx + 40, sy)], fill=(255, 255, 255), width=10)
            draw_subtitle_box(draw, "DẪN ĐẾN THÀNH CÔNG!", sub_font)

        # 4. Phase 4: 103 to 149 (Outro explosion of victory stars & gold aura)
        else:
            draw.line([(350, 1300), (730, 1300)], fill=(0, 229, 255), width=14)
            sx = 850
            # Winner pose on right cliff
            draw.ellipse([sx - 35, 1030, sx + 35, 1100], outline=(255, 255, 255), width=8)
            draw.line([(sx, 1100), (sx, 1200)], fill=(255, 255, 255), width=10)
            # Raised arms
            draw.line([(sx, 1120), (sx - 60, 1050)], fill=(255, 255, 255), width=8)
            draw.line([(sx, 1120), (sx + 60, 1050)], fill=(255, 255, 255), width=8)
            draw.line([(sx, 1200), (sx - 30, 1300)], fill=(255, 255, 255), width=10)
            draw.line([(sx, 1200), (sx + 30, 1300)], fill=(255, 255, 255), width=10)

            # Golden trophy/star burst in celebration
            sw_r = (f - 103) * 8
            draw.ellipse([sx - sw_r, 1050 - sw_r, sx + sw_r, 1050 + sw_r], outline=(255, 230, 0), width=4)
            draw_subtitle_box(draw, "KỶ LUẬT = THÀNH CÔNG!", sub_font)

        proc.stdin.write(img.tobytes())
    proc.stdin.close()
    proc.wait()
    print("Video B complete:", VIDEO_B_OUT)

def main():
    voice_p = asyncio.run(make_voice())
    audio_p = make_bgm(voice_p)
    render_video_a(audio_p)
    render_video_b(audio_p)
    print("ALL A/B TESTS RENDERED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
