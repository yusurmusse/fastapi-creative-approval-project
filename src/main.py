from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io
from src.rules import format_checker, gif_size_checker, minimum_image_size, check_ratio_size, check_legality_and_contrast
from pydantic import BaseModel
from typing import Optional
import logging
from openai import OpenAI
import os

openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key) if openai_key else None

app = FastAPI()
logger = logging.getLogger(__name__)

@app.get("/health")
def health():
    logger.info("Checking health check...")
    return {"status": "Good"}

class Metadata(BaseModel):
    market: Optional[str]
    placement: Optional[str]

class StatusResponse(BaseModel):
    status: str
    reasons: list[str]
    width: int
    height: int
    format: str
    metadata: Optional[Metadata] = None

@app.post("/creative-approval", response_model=StatusResponse)
async def creative_approval(
 
    file: UploadFile = File(...),
    metadata: Optional[Metadata] = None
):
    logger.info("File uploaded successfully %s with metadata %s", file.filename, metadata)
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid input")

    finalStatus = "APPROVED"
    reasons: list[str] = []

    for imageChecker in [format_checker, gif_size_checker,  minimum_image_size, check_ratio_size, check_legality_and_contrast]:
        status, rule_reasons = imageChecker(image)
        reasons.extend(rule_reasons)

        if status == "REJECTED":
            finalStatus = "REJECTED"
        elif status == "REQUIRES_REVIEW" and finalStatus != "REJECTED":
            finalStatus = "REQUIRES_REVIEW"

    return StatusResponse(    
        status=finalStatus,
        reasons=reasons,
        width=image.width,
        height=image.height,
        format=image.format,
        metadata=metadata
)