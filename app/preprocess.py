import torch
from typing import Literal

ProductQuality = Literal["L", "M", "H"]

# OrdinalEncoder(categories=[["L", "M", "H"]])
PRODUCT_QUALITY_ENCODING: dict[str, float] = {
    "L": 0.0,
    "M": 1.0,
    "H": 2.0,
}

FEATURE_ORDER = [
    "product_quality",
    "air_temperature",
    "process_temperature",
    "rotational_speed",
    "torque",
    "tool_wear",
]


def build_feature_tensor(
    *,
    product_quality: ProductQuality,
    air_temperature: float,
    process_temperature: float,
    rotational_speed: float,
    torque: float,
    tool_wear: float,
) -> torch.Tensor:
    values = [
        PRODUCT_QUALITY_ENCODING[product_quality],
        air_temperature,
        process_temperature,
        rotational_speed,
        torque,
        tool_wear,
    ]
    return torch.tensor([values], dtype=torch.float32)
