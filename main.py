from fastapi import FastAPI, UploadFile, File
from gif_generator import gerar_gif
import io
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/gerar-gif")
async def criar_gif(files: list[UploadFile] = File(...)):
    imagens = [await f.read() for f in files]
    gif_bytes = gerar_gif(imagens)
    return StreamingResponse(io.BytesIO(gif_bytes), media_type="image/gif")