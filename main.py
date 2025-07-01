from fastapi import FastAPI, UploadFile, File
from gif_generator import gerar_gif

app = FastAPI()

@app.post("/gerar-gif")
async def gerar_gif_endpoint(
    map: UploadFile = File(...),
    clouds_agora: UploadFile = File(...),
    minus_60min: UploadFile = File(...),
    minus_50min: UploadFile = File(...),
    minus_40min: UploadFile = File(...),
    minus_30min: UploadFile = File(...),
    minus_20min: UploadFile = File(...),
    minus_10min: UploadFile = File(...)
):
    return await gerar_gif(
        map, clouds_agora, minus_60min, minus_50min,
        minus_40min, minus_30min, minus_20min, minus_10min
    )
