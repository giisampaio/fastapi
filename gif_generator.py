from PIL import Image
import io

def gerar_gif(imagens_bytes: list[bytes]) -> bytes:
    imagens = [Image.open(io.BytesIO(b)).convert("RGBA") for b in imagens_bytes]
    output = io.BytesIO()
    imagens[0].save(
        output,
        format='GIF',
        save_all=True,
        append_images=imagens[1:],
        duration=600,
        loop=0,
        optimize=True
    )
    output.seek(0)
    return output.read()