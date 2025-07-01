from fastapi import UploadFile
from PIL import Image, ImageChops, ImageDraw, ImageFont
import io

async def gerar_gif(map, clouds_agora, minus_60min, minus_50min, minus_40min, minus_30min, minus_20min, minus_10min):
    order = [
        ("clouds_agora", clouds_agora, "agora"),
        ("minus_60min", minus_60min, "-60 min"),
        ("minus_50min", minus_50min, "-50 min"),
        ("minus_40min", minus_40min, "-40 min"),
        ("minus_30min", minus_30min, "-30 min"),
        ("minus_20min", minus_20min, "-20 min"),
        ("minus_10min", minus_10min, "-10 min"),
        ("clouds_agora", clouds_agora, "agora")
    ]

    map_bytes = await map.read()
    map_img = Image.open(io.BytesIO(map_bytes)).convert("RGBA")
    font = ImageFont.load_default()
    frames = []

    for _, file, label in order:
        raw = await file.read()
        ci = Image.open(io.BytesIO(raw)).convert("RGBA").resize(map_img.size, Image.LANCZOS)
        ci.putalpha(ci.split()[3].point(lambda p: int(p * 0.8)))

        mlt = ImageChops.multiply(map_img, ci)
        ovl = Image.blend(map_img, ci, 0.5)
        frame = Image.blend(mlt, ovl, 0.3).convert("RGBA")

        draw = ImageDraw.Draw(frame)
        w, h = draw.textsize(label, font=font)
        pad = 20
        draw.rectangle([5, 5, 5 + w + pad, 5 + h + pad], fill=(0, 0, 0, 160))
        draw.text((5 + pad // 2, 5 + pad // 2), label, fill="white", font=font)

        frames.append(frame.convert("P", palette=Image.ADAPTIVE))

    out = io.BytesIO()
    frames[0].save(
        out,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=600,
        loop=3,
        optimize=True
    )
    out.seek(0)

    return {
        "filename": "clouds_animation.gif",
        "content_type": "image/gif",
        "gif": out.read()
    }
