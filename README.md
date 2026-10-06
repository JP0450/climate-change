# Climatic

Base de una aplicación climática con Vue 3 en el frontend y FastAPI en el backend.
El panel inicial muestra indicadores ambientales y emisiones semanales de ejemplo.

## Requisitos

- Python 3.10 o superior
- Node.js 20 o superior

## Iniciar el backend

Desde la carpeta del proyecto:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

La API y su documentación interactiva estarán disponibles en:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Estado: `http://localhost:8000/api/health`
- Datos del panel: `http://localhost:8000/api/dashboard`

## Iniciar el frontend

En otra terminal, desde la carpeta del proyecto:

```powershell
cd frontend
npm install
npm run dev
```

Abre la URL que indique Vite (normalmente `http://localhost:5173`). Las peticiones
`/api` se redirigen al backend local en el puerto 8000.
