from typing import Literal

from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    product_quality: Literal["L", "M", "H"] = Field(
        ...,
        description="Ürün kalitesi (L: düşük, M: orta, H: yüksek)",
    )
    air_temperature: float = Field(..., description="Hava sıcaklığı [K]")
    process_temperature: float = Field(..., description="Proses sıcaklığı [K]")
    rotational_speed: float = Field(..., description="Devir hızı [rpm]")
    torque: float = Field(..., description="Tork [Nm]")
    tool_wear: float = Field(..., description="Takım aşınması [min]")


class ClassProbability(BaseModel):
    label: str
    probability: float


class PredictionOutput(BaseModel):
    predicted_class: str
    confidence: float
    probabilities: list[ClassProbability]
