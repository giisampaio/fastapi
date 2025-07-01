from fastapi import FastAPI, UploadFile, File
from gif_generator import gerar_gif
import io
from fastapi.responses import StreamingResponse
from typing import List

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API online. Use POST /gerar-gif"}

@app.post("/gerar-gif")
async def criar_gif(files: List[UploadFile] = File(...)):
    imagens = [await f.read() for f in files]
    gif_bytes = gerar_gif(imagens)
    return StreamingResponse(io.BytesIO(gif_bytes), media_type="image/gif")
