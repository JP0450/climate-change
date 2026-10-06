from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Climatic API",
    description="API inicial para el panel de monitoreo climático.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Climatic API"}


@app.get("/api/dashboard")
def get_dashboard():
    return {
        "location": "Bogotá, Colombia",
        "updated_at": "Hoy, 09:41",
        "metrics": [
            {
                "id": "temperature",
                "label": "Temperatura",
                "value": "18.4",
                "unit": "°C",
                "change": "-1.2°",
                "trend": "down",
                "icon": "temperature",
            },
            {
                "id": "air-quality",
                "label": "Calidad del aire",
                "value": "28",
                "unit": " AQI",
                "change": "Buena",
                "trend": "good",
                "icon": "air",
            },
            {
                "id": "co2",
                "label": "CO₂ atmosférico",
                "value": "421.8",
                "unit": " ppm",
                "change": "+2.4 ppm",
                "trend": "up",
                "icon": "co2",
            },
        ],
        "weekly_emissions": [
            {"day": "Lun", "value": 48},
            {"day": "Mar", "value": 62},
            {"day": "Mié", "value": 42},
            {"day": "Jue", "value": 76},
            {"day": "Vie", "value": 56},
            {"day": "Sáb", "value": 34},
            {"day": "Dom", "value": 46},
        ],
        "emissions": {
            "value": "2.4",
            "unit": "t",
            "period": "de CO₂ esta semana",
            "change": "-12.8%",
        },
        "insight": {
            "title": "Una semana más consciente",
            "description": "Tus emisiones bajaron un 12.8% respecto a la semana pasada. Pequeños cambios, un impacto real.",
        },
    }
