# gif_generator.py

from PIL import Image, ImageChops, ImageDraw, ImageFont
import io, base64

def gerar_gif(files):
    def read_upload(file):
        return file.file.read()

    map_data = read_upload(files["map"])
    map_img = Image.open(io.BytesIO(map_data)).convert("RGBA")

    order = [
        "clouds_agora",
        "minus_60min", "minus_50min", "minus_40min",
        "minus_30min", "minus_20min", "minus_10min",
        "clouds_agora"
    ]
    labels = ["agora", "-60 min", "-50 min", "-40 min", "-30 min", "-20 min", "-10 min", "agora"]
    font = ImageFont.load_default()

    frames = []
    for name, label in zip(order, labels):
        if name not in files:
            continue
        img_data = read_upload(files[name])
        ci = Image.open(io.BytesIO(img_data)).convert("RGBA").resize(map_img.size, Image.LANCZOS)
        ci.putalpha(ci.split()[3].point(lambda p: int(p * 0.8)))
        mlt = ImageChops.multiply(map_img, ci)
        ovl = Image.blend(map_img, ci, 0.5)
        frame = Image.blend(mlt, ovl, 0.3).convert("RGBA")
        draw = ImageDraw.Draw(frame)
        w, h = draw.textsize(label, font=font)
        draw.rectangle([5, 5, 5 + w + 20, 5 + h + 20], fill=(0, 0, 0, 160))
        draw.text((15, 15), label, fill="white", font=font)
        frames.append(frame.convert("P", palette=Image.ADAPTIVE))

    out = io.BytesIO()
    frames[0].save(out, format="GIF", save_all=True, append_images=frames[1:], duration=600, loop=3, optimize=True)
    out.seek(0)

    return {
        "filename": "clouds_animation.gif",
        "mime_type": "image/gif",
        "data": base64.b64encode(out.read()).decode()
    }
