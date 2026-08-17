import torch
import torch.nn as nn
from pathlib import Path

# sklearn LabelEncoder alfabetik sıralama — 09-WebAppOdeviModel.ipynb ile aynı
CLASS_LABELS = [
    "Heat Dissipation Failure",
    "No Failure",
    "Overstrain Failure",
    "Power Failure",
    "Random Failures",
    "Tool Wear Failure",
]

MODEL_PATH = Path(__file__).resolve().parent.parent / "models2" / "predictive_maintenance_classification_model.pth"


class FailureClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_layer_stack = nn.Sequential(
            nn.Linear(in_features=6, out_features=50),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(in_features=50, out_features=45),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(in_features=45, out_features=6),
        )

    def forward(self, x):
        return self.linear_layer_stack(x)


def load_model() -> FailureClassifier:
    model = FailureClassifier()
    state_dict = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
    model.load_state_dict(state_dict)
    model.eval()
    return model
