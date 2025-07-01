from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import List
from gif_generator import gerar_gif
import io

app = FastAPI()

@app.post("/gerar-gif")
async def criar_gif(
    map: UploadFile = File(...),
    clouds_agora: UploadFile = File(...),
    minus_60min: UploadFile = File(...),
    minus_50min: UploadFile = File(...),
    minus_40min: UploadFile = File(...),
    minus_30min: UploadFile = File(...),
    minus_20min: UploadFile = File(...),
    minus_10min: UploadFile = File(...)
):
    files = {
        "map": await map.read(),
        "clouds_agora": await clouds_agora.read(),
        "minus_60min": await minus_60min.read(),
        "minus_50min": await minus_50min.read(),
        "minus_40min": await minus_40min.read(),
        "minus_30min": await minus_30min.read(),
        "minus_20min": await minus_20min.read(),
        "minus_10min": await minus_10min.read(),
    }

    gif_bytes = gerar_gif(files)
    return StreamingResponse(io.BytesIO(gif_bytes), media_type="image/gif")
