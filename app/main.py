from contextlib import asynccontextmanager
from pathlib import Path

import torch
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.model import CLASS_LABELS, load_model
from app.preprocess import build_feature_tensor
from app.schemas import ClassProbability, PredictionInput, PredictionOutput

BASE_DIR = Path(__file__).resolve().parent.parent

model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model = load_model()
    yield


app = FastAPI(
    title="Predictive Maintenance API",
    description="Makine arıza türü sınıflandırma servisi",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")
templates.env.auto_reload = True


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "class_labels": CLASS_LABELS,
        },
    )

@app.post("/predict", response_model=PredictionOutput)
async def predict(data: PredictionInput):
    features = build_feature_tensor(
        product_quality=data.product_quality,
        air_temperature=data.air_temperature,
        process_temperature=data.process_temperature,
        rotational_speed=data.rotational_speed,
        torque=data.torque,
        tool_wear=data.tool_wear,
    )

    with torch.inference_mode():
        logits = model(features)
        probabilities = torch.softmax(logits, dim=1)[0]
        predicted_idx = int(probabilities.argmax().item())

    return PredictionOutput(
        predicted_class=CLASS_LABELS[predicted_idx],
        confidence=round(float(probabilities[predicted_idx].item()) * 100, 2),
        probabilities=[
            ClassProbability(
                label=label,
                probability=round(float(prob.item()) * 100, 2),
            )
            for label, prob in zip(CLASS_LABELS, probabilities)
        ],
    )


@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": model is not None}
