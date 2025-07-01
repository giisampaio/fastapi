from PIL import Image
from io import BytesIO
from fastapi import UploadFile, File
from fastapi.responses import StreamingResponse
from typing import List

@app.post("/gerar-gif")
async def gerar_gif(files: List[UploadFile] = File(...)):
    imagens = []
    for file in files:
        conteudo = await file.read()
        imagem = Image.open(BytesIO(conteudo))

        # Força conversão para RGBA se necessário
        if imagem.mode != "RGBA":
            imagem = imagem.convert("RGBA")

        imagens.append(imagem)

    # Cria o GIF
    output = BytesIO()
    imagens[0].save(output, format="GIF", save_all=True, append_images=imagens[1:], duration=500, loop=0)
    output.seek(0)
    
    return StreamingResponse(output, media_type="image/gif")
