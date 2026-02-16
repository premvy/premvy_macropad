from PIL import Image, ImageSequence
import os

threshold = 170 # how much "black" should be turned into a black pixel

TARGET_W = 128
TARGET_H = 32
    
gif_path = "PATH_HERE"
output_dir = "PATH_HERE"

os.makedirs(output_dir, exist_ok=True)

img = Image.open(gif_path)
frame_count = 0

for i, frame in enumerate(ImageSequence.Iterator(img)):
    frame = frame.copy()

    bw = frame.convert("L").point(
        lambda x: 0 if x > threshold else 255,
        mode="1"
    )

    canvas = Image.new("1", (TARGET_W, TARGET_H), 0)

    offset_x = (TARGET_W - bw.width) // 2
    offset_y = (TARGET_H - bw.height) // 2

    canvas.paste(bw, (offset_x, offset_y))

    output_path = os.path.join(output_dir, f"frame_{i}.bmp")
    canvas.save(output_path, format="BMP")

    frame_count += 1
