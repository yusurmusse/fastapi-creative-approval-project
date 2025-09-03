from fastapi.testclient import TestClient
from PIL import Image
import io
from src.main import app

client = TestClient(app)

def test_approval():
    imageBytes = io.BytesIO()
    image = Image.new("L", (500,300), color=200)
    image.save(imageBytes, format="PNG")
    imageBytes.seek(0)

    response = client.post(
            "/creative-approval",
            files={"file": ("test_approval.png", imageBytes, "image/png")}
        )
    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED"

def test_rejection():
    imageBytes = io.BytesIO()
    image = Image.new("L", (500,500), color=200)
    image.save(imageBytes, format="GIF")
    imageBytes.seek(0)

    response = client.post(
            "/creative-approval",
            files={"file": ("test_rejection.gif", imageBytes, "image/gif")}
        )
    assert response.status_code == 200
    assert response.json()["status"] == "REJECTED"

def test_error_missing_file():
    response = client.post(
            "/creative-approval",
            files={}
        )
    assert response.status_code == 422   
