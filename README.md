# Predictive Maintenance Web App

Makine bakım verilerinden arıza türünü tahmin eden PyTorch tabanlı sınıflandırma uygulaması. 

## Özellikler

- **FastAPI** REST API (`POST /predict`, `GET /health`)
- **Web arayüzü** — sensör değerlerini girerek anlık tahmin
- **PyTorch MLP** — 6 girdi → 50 → 45 → 6 sınıf (Dropout 0.3)

## Model ve Veri Ön İşleme

| Özellik | Açıklama |
|---------|----------|
| `product_quality` | L / M / H → OrdinalEncoder ile 0 / 1 / 2 |
| `air_temperature` | Hava sıcaklığı [K] |
| `process_temperature` | Proses sıcaklığı [K] |
| `rotational_speed` | Devir hızı [rpm] |
| `torque` | Tork [Nm] |
| `tool_wear` | Takım aşınması [min] |

Tahmin edilen sınıflar (`LabelEncoder` alfabetik sıra):

1. Heat Dissipation Failure  
2. No Failure  
3. Overstrain Failure  
4. Power Failure  
5. Random Failures  
6. Tool Wear Failure  

## Kurulum

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

```
models2/predictive_maintenance_classification_model.pth
```

## Çalıştırma

Proje kök dizininden:

```bash
uvicorn app.main:app --reload
```

Tarayıcıda: [http://127.0.0.1:8000](http://127.0.0.1:8000)

API dokümantasyonu: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Örneği

```bash
curl -X POST "http://127.0.0.1:8000/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"product_quality\":\"M\",\"air_temperature\":298.1,\"process_temperature\":308.6,\"rotational_speed\":1551,\"torque\":42.8,\"tool_wear\":0}"
```

Örnek yanıt:

```json
{
  "predicted_class": "No Failure",
  "confidence": 100.0,
  "probabilities": [
    {"label": "Heat Dissipation Failure", "probability": 0.0},
    {"label": "No Failure", "probability": 100.0},
    ...
  ]
}
```

## Proje Yapısı

```
web-app-odevi/
├── app/
│   ├── main.py          # FastAPI uygulaması
│   ├── model.py         # PyTorch model tanımı ve yükleme
│   ├── preprocess.py    # Özellik vektörü oluşturma
│   └── schemas.py       # Pydantic istek/yanıt modelleri
├── models2/
│   └── predictive_maintenance_classification_model.pth
├── static/              # CSS ve JavaScript
├── templates/           # HTML şablonları
└── requirements.txt
```

## Notlar

- Bu proje derin öğrenme kursu ödevi kapsamında eğitim amaçlı geliştirilmiştir.

