import asyncio
import edge_tts
import json
import os
import sys

TEXT = "Đừng bao giờ cúi đầu trước bão giông. Mỗi vết sẹo trên người bạn là bằng chứng của một lần bạn đã kiên cường vượt qua. Người khác có thể nghi ngờ bạn. Hoàn cảnh có thể vùi dập bạn. Nhưng chừng nào bạn chưa bỏ cuộc, bạn vẫn là kẻ bất khả chiến bại. Hãy đứng dậy, tiến về phía trước và biến áp lực thành kim cương!"

async def generate_voice(out_mp3, out_vtt):
    comm = edge_tts.Communicate(TEXT, "vi-VN-HoaiMyNeural", rate="+5%")
    sub_maker = edge_tts.SubMaker()
    with open(out_mp3, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                sub_maker.feed(chunk)
    with open(out_vtt, "w", encoding="utf-8") as f:
        f.write(sub_maker.get_srt())
    print("TTS & Subtitles generated successfully!")

if __name__ == "__main__":
    out_dir = "C:/Users/Admin/JavisOS/brains/Brain Default/scratch/openmotion_stickman"
    os.makedirs(out_dir, exist_ok=True)
    asyncio.run(generate_voice(f"{out_dir}/voice.mp3", f"{out_dir}/subtitles.srt"))
