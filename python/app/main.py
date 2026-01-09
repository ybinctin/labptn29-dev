from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io

from app.image_processor import ImageProcessor
from app.config_loader import charger_config

app = FastAPI()

config = charger_config()
processor = ImageProcessor(**config)

@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    image_redim = processor.redimensionner(image)

    output_path = "output.jpg"
    success = processor.compresser(image_redim, output_path)

    if not success:
        return {"error": "Compression impossible"}

    return {"status": "image traitée avec succès"}
