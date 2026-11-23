import math
import os
import random
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SCRATCH_DIR = "C:/Users/Admin/JavisOS/brains/Brain Default/scratch/openmotion_stickman"
OUTPUT_DIR = "C:/Users/Admin/JavisOS/brains/Brain Default/attachments/video-production"
OUTPUT_MP4 = os.path.join(OUTPUT_DIR, "dong_luc_nguoi_que.mp4")
FONT_PATH = "C:/Windows/Fonts/segoeuib.ttf"
TITLE_FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"

TOTAL_SECONDS = 20.0
FPS = 30
TOTAL_FRAMES = int(TOTAL_SECONDS * FPS)  # 600 frames
WIDTH = 1080
HEIGHT = 1920

def generate_cinematic_audio():
    sr = 44100
    t = np.linspace(0, TOTAL_SECONDS, int(sr * TOTAL_SECONDS), endpoint=False)
    audio = np.zeros_like(t)

    # 1. Bassline progression (A minor feel: A1 -> F1 -> G1 -> E1)
    chords = [(0.0, 3.5, 55.0), (3.5, 8.5, 43.65), (8.5, 15.0, 49.0), (15.0, 20.0, 65.4)]
    for start, end, freq in chords:
        mask = (t >= start) & (t < end)
        t_seg = t[mask] - start
        # Sub-bass + harmonic
        sub = 0.25 * np.sin(2 * np.pi * freq * t_seg)
        harm = 0.12 * np.sin(2 * np.pi * freq * 2 * t_seg)
        # Low frequency pulse (LFO)
        lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 4 * t_seg)
        audio[mask] += (sub + harm) * (0.8 + 0.2 * lfo)

    # 2. Epic Kick drum hits (on beat: every 0.6s)
    beat_interval = 0.6
    num_beats = int(TOTAL_SECONDS / beat_interval)
    for b in range(num_beats):
        bt = b * beat_interval
        dur = 0.25
        mask = (t >= bt) & (t < bt + dur)
        if np.any(mask):
            t_k = t[mask] - bt
            # Pitch drop 130Hz -> 45Hz
            k_freq = 45 + 85 * np.exp(-t_k * 25)
            phase = 2 * np.pi * np.cumsum(k_freq) / sr
            kick = 0.35 * np.sin(phase) * np.exp(-t_k * 12)
            audio[mask] += kick

    # 3. Transitions & Impacts (Whoosh & Boom at scene cuts: 0s, 3.5s, 8.5s, 15.0s)
    transition_times = [0.0, 3.5, 8.5, 15.0]
    for tr in transition_times:
        dur = 1.2
        mask = (t >= tr) & (t < tr + dur)
        if np.any(mask):
            t_tr = t[mask] - tr
            # Low rumble + noise
            noise = np.random.uniform(-0.15, 0.15, len(t_tr)) * np.exp(-t_tr * 3)
            boom = 0.4 * np.sin(2 * np.pi * 50 * t_tr) * np.exp(-t_tr * 3.5)
            audio[mask] += noise + boom

    # 4. Climax Riser (from 13.0s to 15.2s)
    riser_mask = (t >= 13.0) & (t < 15.2)
    if np.any(riser_mask):
        t_r = t[riser_mask] - 13.0
        r_freq = 200 + 600 * (t_r / 2.2)**2
        phase_r = 2 * np.pi * np.cumsum(r_freq) / sr
        riser = 0.18 * np.sin(phase_r) * (t_r / 2.2)
        audio[riser_mask] += riser

    # Master limiter & normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.75  # leave headroom for voiceover

    # Convert to 16-bit PCM
    audio_int16 = (audio * 32767).astype(np.int16)
    wav_path = os.path.join(SCRATCH_DIR, "bgm_track.wav")
    
    import wave
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_int16.tobytes())
    print("BGM wav generated:", wav_path)
    return wav_path

def mix_full_audio(bgm_wav):
    # Scene voice files
    s1 = os.path.join(SCRATCH_DIR, "scene1.mp3")
    s2 = os.path.join(SCRATCH_DIR, "scene2.mp3")
    s3 = os.path.join(SCRATCH_DIR, "scene3.mp3")
    s4 = os.path.join(SCRATCH_DIR, "scene4.mp3")
    out_audio = os.path.join(SCRATCH_DIR, "final_audio.mp3")

    # Delays: s1=0.3s, s2=3.6s, s3=8.7s, s4=15.2s
    # FFmpeg adelay filter takes delay in milliseconds
    filter_str = (
        "[1:a]adelay=300|300,volume=1.35[v1];"
        "[2:a]adelay=3600|3600,volume=1.35[v2];"
        "[3:a]adelay=8700|8700,volume=1.35[v3];"
        "[4:a]adelay=15200|15200,volume=1.35[v4];"
        "[0:a]volume=0.6[bgm];"
        "[bgm][v1][v2][v3][v4]amix=inputs=5:duration=first:dropout_transition=2[outa]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", bgm_wav,
        "-i", s1, "-i", s2, "-i", s3, "-i", s4,
        "-filter_complex", filter_str,
        "-map", "[outa]",
        "-c:a", "libmp3lame", "-b:a", "192k",
        out_audio
    ]
    subprocess.check_call(cmd)
    print("Mixed audio ready:", out_audio)
    return out_audio

# --- Stickman & Scene Drawing Helpers ---

def draw_glow_line(draw, pt1, pt2, color=(255, 255, 255), width=8, glow_color=(0, 229, 255), glow_width=20):
    # Draw glow layer
    draw.line([pt1, pt2], fill=glow_color, width=glow_width)
    # Draw sharp center core
    draw.line([pt1, pt2], fill=color, width=width)

def draw_glow_circle(draw, center, radius, color=(255, 255, 255), outline=8, glow_color=(0, 229, 255), glow_width=18):
    cx, cy = center
    # Outer glow ring
    draw.ellipse([cx - radius - glow_width, cy - radius - glow_width, cx + radius + glow_width, cy + radius + glow_width], outline=glow_color, width=glow_width)
    # Center ring / fill
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=color, width=outline)

def draw_stickman(draw, x, y, pose):
    """
    pose: dict containing angles and offsets
    head_center, shoulder, elbow_l, hand_l, elbow_r, hand_r, pelvis, knee_l, foot_l, knee_r, foot_r
    """
    scale = pose.get("scale", 1.0)
    glow_col = pose.get("glow", (0, 229, 255))
    core_col = (255, 255, 255)
    
    # Coordinates relative to (x, y) pelvis
    pelvis = (x, y)
    shoulder = (x + pose.get("spine_dx", 0) * scale, y - 180 * scale)
    head_center = (shoulder[0] + pose.get("neck_dx", 0) * scale, shoulder[1] - 80 * scale)
    head_rad = int(50 * scale)
    
    # Head
    draw_glow_circle(draw, head_center, head_rad, color=core_col, outline=10, glow_color=glow_col, glow_width=16)
    
    # Eyes glow (two dots)
    eye_dx = pose.get("eye_dir", 1) * 15 * scale
    eye_y = head_center[1] - 5 * scale
    draw.ellipse([head_center[0] + eye_dx - 6, eye_y - 6, head_center[0] + eye_dx + 6, eye_y + 6], fill=(255, 230, 0))

    # Spine
    draw_glow_line(draw, pelvis, shoulder, color=core_col, width=12, glow_color=glow_col, glow_width=22)

    # Left arm
    elbow_l = (shoulder[0] + pose.get("el_l_x", -60) * scale, shoulder[1] + pose.get("el_l_y", 80) * scale)
    hand_l = (elbow_l[0] + pose.get("h_l_x", -40) * scale, elbow_l[1] + pose.get("h_l_y", 70) * scale)
    draw_glow_line(draw, shoulder, elbow_l, color=core_col, width=10, glow_color=glow_col, glow_width=18)
    draw_glow_line(draw, elbow_l, hand_l, color=core_col, width=10, glow_color=glow_col, glow_width=18)

    # Right arm
    elbow_r = (shoulder[0] + pose.get("el_r_x", 60) * scale, shoulder[1] + pose.get("el_r_y", 80) * scale)
    hand_r = (elbow_r[0] + pose.get("h_r_x", 40) * scale, elbow_r[1] + pose.get("h_r_y", 70) * scale)
    draw_glow_line(draw, shoulder, elbow_r, color=core_col, width=10, glow_color=glow_col, glow_width=18)
    draw_glow_line(draw, elbow_r, hand_r, color=core_col, width=10, glow_color=glow_col, glow_width=18)

    # Left leg
    knee_l = (pelvis[0] + pose.get("kn_l_x", -50) * scale, pelvis[1] + pose.get("kn_l_y", 110) * scale)
    foot_l = (knee_l[0] + pose.get("ft_l_x", -20) * scale, knee_l[1] + pose.get("ft_l_y", 120) * scale)
    draw_glow_line(draw, pelvis, knee_l, color=core_col, width=12, glow_color=glow_col, glow_width=20)
    draw_glow_line(draw, knee_l, foot_l, color=core_col, width=12, glow_color=glow_col, glow_width=20)

    # Right leg
    knee_r = (pelvis[0] + pose.get("kn_r_x", 50) * scale, pelvis[1] + pose.get("kn_r_y", 110) * scale)
    foot_r = (knee_r[0] + pose.get("ft_r_x", 20) * scale, knee_r[1] + pose.get("ft_r_y", 120) * scale)
    draw_glow_line(draw, pelvis, knee_r, color=core_col, width=12, glow_color=glow_col, glow_width=20)
    draw_glow_line(draw, knee_r, foot_r, color=core_col, width=12, glow_color=glow_col, glow_width=20)

    return {"pelvis": pelvis, "shoulder": shoulder, "head": head_center, "hand_l": hand_l, "hand_r": hand_r}

def draw_subtitle(draw, text, font):
    # Box parameters
    box_w = 980
    box_h = 160
    box_x = (WIDTH - box_w) // 2
    box_y = 1650
    
    # Semi-transparent dark background card
    card_bg = (15, 23, 42)
    border_col = (0, 229, 255)
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=24, fill=card_bg, outline=border_col, width=4)
    
    # Word wrap if needed or center single/two lines
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    if tw > box_w - 60:
        # split in half
        words = text.split(" ")
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        
        b1 = font.getbbox(line1)
        b2 = font.getbbox(line2)
        tx1 = box_x + (box_w - (b1[2]-b1[0])) // 2
        tx2 = box_x + (box_w - (b2[2]-b2[0])) // 2
        ty1 = box_y + 22
        ty2 = box_y + 82
        
        # Draw shadow + text
        for dx, dy in [(-2,-2), (2,-2), (-2,2), (2,2), (0,3)]:
            draw.text((tx1+dx, ty1+dy), line1, font=font, fill=(0, 0, 0))
            draw.text((tx2+dx, ty2+dy), line2, font=font, fill=(0, 0, 0))
        draw.text((tx1, ty1), line1, font=font, fill=(255, 230, 0))
        draw.text((tx2, ty2), line2, font=font, fill=(255, 230, 0))
    else:
        tx = box_x + (box_w - tw) // 2
        ty = box_y + (box_h - th) // 2 - 8
        for dx, dy in [(-2,-2), (2,-2), (-2,2), (2,2), (0,3)]:
            draw.text((tx+dx, ty+dy), text, font=font, fill=(0, 0, 0))
        draw.text((tx, ty), text, font=font, fill=(255, 230, 0))

def main():
    print("Generating cinematic audio...")
    bgm_wav = generate_cinematic_audio()
    mixed_audio = mix_full_audio(bgm_wav)

    print("Setting up font and video stream...")
    sub_font = ImageFont.truetype(FONT_PATH, 46)
    header_font = ImageFont.truetype(TITLE_FONT_PATH, 32)

    # Launch FFmpeg process to receive rawvideo from pipe
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",  # pipe from stdin
        "-i", mixed_audio,
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "21",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_MP4
    ]
    ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    # Particle system state
    particles = []
    for _ in range(60):
        particles.append({
            "x": random.randint(50, WIDTH - 50),
            "y": random.randint(100, HEIGHT - 200),
            "vx": random.uniform(-0.5, 0.5),
            "vy": random.uniform(-2.5, -0.8),
            "rad": random.randint(2, 5),
            "alpha": random.randint(100, 255)
        })

    # Render loop
    print(f"Rendering {TOTAL_FRAMES} frames...")
    floor_y = 1450

    for f_idx in range(TOTAL_FRAMES):
        t_sec = f_idx / FPS
        # Create base canvas with dark cyber gradient
        img = Image.new("RGB", (WIDTH, HEIGHT), (8, 12, 22))
        draw = ImageDraw.Draw(img)

        # Subtle background grid & floor
        draw.line([(0, floor_y), (WIDTH, floor_y)], fill=(30, 58, 138), width=4)
        for gx in range(0, WIDTH, 120):
            draw.line([(gx, floor_y), (gx + (gx - WIDTH//2)*0.8, HEIGHT)], fill=(15, 23, 42), width=2)

        # Header tag
        draw.text((WIDTH // 2 - 220, 100), "⚡ OPENMOTION • NĂNG LƯỢNG BỨT PHÁ", font=header_font, fill=(0, 229, 255))

        # Floating ambient energy particles
        for p in particles:
            p["y"] += p["vy"]
            p["x"] += p["vx"]
            if p["y"] < 150:
                p["y"] = floor_y - random.randint(10, 50)
                p["x"] = random.randint(50, WIDTH - 50)
            col = (0, 229, 255) if random.random() > 0.3 else (255, 230, 0)
            draw.ellipse([p["x"] - p["rad"], p["y"] - p["rad"], p["x"] + p["rad"], p["y"] + p["rad"]], fill=col)

        # ==================== SCENE 1: Bão giông (Frames 0 - 104, 3.5s) ====================
        if f_idx < 105:
            # Rain streaks
            for _ in range(35):
                rx = random.randint(0, WIDTH + 200)
                ry = random.randint(100, floor_y)
                draw.line([(rx, ry), (rx - 25, ry + 40)], fill=(70, 95, 130), width=2)
            
            # Lightning flash at frame 40-44
            if 40 <= f_idx <= 44:
                # White lightning bolt
                draw.line([(500, 100), (560, 400), (520, 600), (600, 900), (540, 1200)], fill=(255, 255, 255), width=8)
                draw.line([(500, 100), (560, 400), (520, 600), (600, 900), (540, 1200)], fill=(0, 229, 255), width=20)

            # Stickman: rises from crouch to proud standing
            progress = min(1.0, max(0.0, (f_idx - 35) / 50.0))
            # Spine interpolation
            spine_dx = -40 * (1.0 - progress)
            neck_dx = -30 * (1.0 - progress)
            eye_dir = -1 if progress < 0.5 else 1
            glow_c = (0, 229, 255) if progress > 0.6 else (100, 116, 139)

            pose = {
                "spine_dx": spine_dx, "neck_dx": neck_dx, "eye_dir": eye_dir, "glow": glow_c,
                "el_l_x": -50 - 20*progress, "el_l_y": 70 - 40*progress,
                "h_l_x": -30, "h_l_y": 60 - 50*progress,
                "el_r_x": 40 + 30*progress, "el_r_y": 70 - 40*progress,
                "h_r_x": 30, "h_r_y": 60 - 50*progress,
                "kn_l_x": -50 + 10*progress, "kn_l_y": 100 + 10*progress,
                "ft_l_x": -30, "ft_l_y": 110,
                "kn_r_x": 50 - 10*progress, "kn_r_y": 100 + 10*progress,
                "ft_r_x": 30, "ft_r_y": 110
            }
            # Y position elevates as standing up
            sm_y = floor_y - 230 - int(progress * 40)
            res = draw_stickman(draw, 540, sm_y, pose)
            
            # Fire energy aura around hands at peak
            if progress > 0.7:
                for h in [res["hand_l"], res["hand_r"]]:
                    for _ in range(6):
                        fx = h[0] + random.randint(-15, 15)
                        fy = h[1] + random.randint(-25, 10)
                        draw.ellipse([fx-8, fy-8, fx+8, fy+8], fill=(255, 230, 0))

            draw_subtitle(draw, "ĐỪNG BAO GIỜ CÚI ĐẦU TRƯỚC BÃO GIÔNG!", sub_font)

        # ==================== SCENE 2: Kiên cường & Bứt phá (Frames 105 - 254, 5.0s) ====================
        elif f_idx < 255:
            s2_frame = f_idx - 105
            # Draw steep mountain slope
            draw.polygon([(0, floor_y), (WIDTH, floor_y - 450), (WIDTH, floor_y), (0, floor_y)], fill=(17, 24, 39))
            draw.line([(0, floor_y), (WIDTH, floor_y - 450)], fill=(0, 229, 255), width=6)

            shattered = s2_frame > 75
            walk_cycle = math.sin(s2_frame * 0.25)
            
            # Stickman walking up the slope
            pos_x = 350 + min(200, s2_frame * 1.5)
            slope_h = (pos_x / WIDTH) * 450
            sm_y = floor_y - int(slope_h) - 220

            if not shattered:
                # Carrying giant glowing rock on back
                boulder_center = (pos_x - 70, sm_y - 260)
                draw.ellipse([boulder_center[0]-140, boulder_center[1]-140, boulder_center[0]+140, boulder_center[1]+140], fill=(30, 41, 59), outline=(245, 158, 11), width=10)
                # Glowing stress cracks
                draw.line([(boulder_center[0]-60, boulder_center[1]-40), (boulder_center[0], boulder_center[1]+20), (boulder_center[0]+70, boulder_center[1]-30)], fill=(255, 230, 0), width=6)
                draw.line([(boulder_center[0]-20, boulder_center[1]+10), (boulder_center[0]+30, boulder_center[1]+80)], fill=(255, 230, 0), width=5)

                pose = {
                    "spine_dx": 45, "neck_dx": 30, "eye_dir": 1, "glow": (245, 158, 11),
                    "el_l_x": -60, "el_l_y": -50, "h_l_x": -30, "h_l_y": -60,
                    "el_r_x": -20, "el_r_y": -60, "h_r_x": -10, "h_r_y": -60,
                    "kn_l_x": -40 + int(walk_cycle * 25), "kn_l_y": 100,
                    "ft_l_x": -10, "ft_l_y": 110,
                    "kn_r_x": 40 - int(walk_cycle * 25), "kn_r_y": 100,
                    "ft_r_x": 10, "ft_r_y": 110
                }
            else:
                # Rock has exploded! Golden shockwave and debris expanding
                explode_t = s2_frame - 75
                draw_glow_circle(draw, (pos_x - 30, sm_y - 240), int(explode_t * 18), color=(255, 255, 255), outline=8, glow_color=(255, 230, 0), glow_width=25)
                # Flying fragments
                for i in range(16):
                    ang = i * (2 * math.pi / 16)
                    fx = pos_x - 30 + math.cos(ang) * explode_t * 14
                    fy = sm_y - 240 + math.sin(ang) * explode_t * 14
                    draw.ellipse([fx-10, fy-10, fx+10, fy+10], fill=(255, 230, 0))

                # Stickman standing tall, triumphant
                pose = {
                    "spine_dx": 10, "neck_dx": 0, "eye_dir": 1, "glow": (255, 230, 0),
                    "el_l_x": -80, "el_l_y": -60, "h_l_x": -30, "h_l_y": -50,
                    "el_r_x": 80, "el_r_y": -60, "h_r_x": 30, "h_r_y": -50,
                    "kn_l_x": -50, "kn_l_y": 110, "ft_l_x": -20, "ft_l_y": 110,
                    "kn_r_x": 50, "kn_r_y": 110, "ft_r_x": 20, "ft_r_y": 110
                }

            draw_stickman(draw, int(pos_x), sm_y, pose)
            draw_subtitle(draw, "MỖI VẾT SẸO LÀ BẰNG CHỨNG CỦA SỰ KIÊN CƯỜNG!", sub_font)

        # ==================== SCENE 3: Bất khả chiến bại (Frames 255 - 449, 6.5s) ====================
        elif f_idx < 450:
            s3_frame = f_idx - 255
            center_x = 540
            sm_y = floor_y - 240
            
            # Energy Shield dome around stickman
            shield_r = 280 + int(math.sin(s3_frame * 0.2) * 12)
            draw_glow_circle(draw, (center_x, sm_y - 80), shield_r, color=(255, 255, 255), outline=10, glow_color=(0, 229, 255), glow_width=28)
            
            # Multiple incoming obstacle arrows / energy spikes
            for i in range(5):
                arrow_t = (s3_frame * 18 + i * 180) % 700
                from_left = (i % 2 == 0)
                if from_left:
                    ax = 50 + arrow_t
                    ay = sm_y - 180 + i * 60
                    # Hit shield check
                    if ax >= center_x - shield_r:
                        # Spark explosion at impact point
                        for _ in range(8):
                            spx = center_x - shield_r + random.randint(-15, 25)
                            spy = ay + random.randint(-20, 20)
                            draw.ellipse([spx-6, spy-6, spx+6, spy+6], fill=(255, 0, 85))
                    else:
                        draw_glow_line(draw, (ax - 60, ay), (ax, ay), color=(255, 50, 100), width=8, glow_color=(255, 0, 50), glow_width=16)
                else:
                    ax = WIDTH - 50 - arrow_t
                    ay = sm_y - 220 + i * 70
                    if ax <= center_x + shield_r:
                        for _ in range(8):
                            spx = center_x + shield_r + random.randint(-25, 15)
                            spy = ay + random.randint(-20, 20)
                            draw.ellipse([spx-6, spy-6, spx+6, spy+6], fill=(255, 0, 85))
                    else:
                        draw_glow_line(draw, (ax + 60, ay), (ax, ay), color=(255, 50, 100), width=8, glow_color=(255, 0, 50), glow_width=16)

            # Powerful battle stance
            pose = {
                "spine_dx": 0, "neck_dx": 0, "eye_dir": 1, "glow": (0, 229, 255),
                "el_l_x": -90, "el_l_y": 10, "h_l_x": 30, "h_l_y": -60,
                "el_r_x": 90, "el_r_y": 10, "h_r_x": -30, "h_r_y": -60,
                "kn_l_x": -80, "kn_l_y": 80, "ft_l_x": -30, "ft_l_y": 120,
                "kn_r_x": 80, "kn_r_y": 80, "ft_r_x": 30, "ft_r_y": 120
            }
            draw_stickman(draw, center_x, sm_y, pose)
            draw_subtitle(draw, "CHƯA BỎ CUỘC, BẠN VẪN BẤT KHẢ CHIẾN BẠI!", sub_font)

        # ==================== SCENE 4: Biến áp lực thành kim cương (Frames 450 - 599, 5.0s) ====================
        else:
            s4_frame = f_idx - 450
            # Speed lines across screen
            for _ in range(25):
                lx = random.randint(0, WIDTH)
                ly = random.randint(200, HEIGHT - 300)
                draw.line([(lx, ly), (lx + random.randint(120, 300), ly)], fill=(50, 80, 120), width=3)

            # Giant sparkling 3D diamond at top center (540, 520)
            diamond_x = 540
            diamond_y = 520
            d_rot = s4_frame * 0.08
            
            # Diamond facet wireframe with rotation
            w = 140
            h = 170
            dx_top = diamond_x
            dy_top = diamond_y - h
            dx_bot = diamond_x
            dy_bot = diamond_y + h
            
            # Rotating left/right points
            dl_x = diamond_x - int(w * math.cos(d_rot))
            dr_x = diamond_x + int(w * math.cos(d_rot))
            dm_y = diamond_y - 20
            
            # Halo around diamond
            draw_glow_circle(draw, (diamond_x, diamond_y), 190, color=(255, 255, 255), outline=8, glow_color=(0, 229, 255), glow_width=32)
            
            # Diamond facets
            draw.polygon([(dx_top, dy_top), (dr_x, dm_y), (dx_bot, dy_bot), (dl_x, dm_y)], fill=(15, 45, 80), outline=(255, 255, 255), width=6)
            draw.line([(dx_top, dy_top), (dx_bot, dy_bot)], fill=(0, 229, 255), width=4)
            draw.line([(dl_x, dm_y), (dr_x, dm_y)], fill=(0, 229, 255), width=4)

            # Diamond sparkle glints
            for ang in [0, math.pi/4, math.pi/2, 3*math.pi/4]:
                gl_len = 50 + int(math.sin(s4_frame * 0.3) * 20)
                draw.line([(diamond_x - math.cos(ang)*gl_len, diamond_y - math.sin(ang)*gl_len),
                           (diamond_x + math.cos(ang)*gl_len, diamond_y + math.sin(ang)*gl_len)],
                          fill=(255, 255, 255), width=4)

            # Stickman leaping up towards the diamond
            leap_prog = min(1.0, s4_frame / 70.0)
            leap_x = 250 + int(leap_prog * 240)
            leap_y = floor_y - 200 - int(leap_prog * 650)
            
            # Dynamic mid-air jump pose reaching for diamond
            pose = {
                "spine_dx": 30, "neck_dx": 20, "eye_dir": 1, "glow": (255, 230, 0),
                "el_l_x": 40, "el_l_y": -110, "h_l_x": 30, "h_l_y": -70,  # reaching hand high
                "el_r_x": -40, "el_r_y": 40, "h_r_x": -30, "h_r_y": 60,
                "kn_l_x": -60, "kn_l_y": 70, "ft_l_x": -40, "ft_l_y": 80,
                "kn_r_x": 30, "kn_r_y": 90, "ft_r_x": 30, "ft_r_y": 90
            }
            draw_stickman(draw, leap_x, leap_y, pose)

            # Golden shockwave rings if reached near diamond
            if s4_frame > 65:
                sw_r = (s4_frame - 65) * 14
                draw.ellipse([diamond_x - sw_r, diamond_y - sw_r, diamond_x + sw_r, diamond_y + sw_r], outline=(255, 230, 0), width=6)

            draw_subtitle(draw, "HÃY ĐỨNG DẬY VÀ BIẾN ÁP LỰC THÀNH KIM CƯƠNG!", sub_font)

        # Write frame to FFmpeg pipe
        ffmpeg_proc.stdin.write(img.tobytes())

        if (f_idx + 1) % 100 == 0 or f_idx == TOTAL_FRAMES - 1:
            print(f"Rendered frame {f_idx + 1}/{TOTAL_FRAMES} ({(f_idx+1)/TOTAL_FRAMES*100:.1f}%)")

    ffmpeg_proc.stdin.close()
    ffmpeg_proc.wait()
    print("Video encoding complete!")
    print(f"FINAL OUTPUT: {OUTPUT_MP4}")

if __name__ == "__main__":
    main()
