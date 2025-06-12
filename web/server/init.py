from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Инициализация веб-приложения
app = FastAPI(title="Hackathon Chat API", 
             description="API для чат-приложения хакатона")

# Настройка CORS (в продакшене укажите конкретные домены вместо "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Временное решение для разработки
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Конфигурация путей
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "hakaton", "static")  # Переименовано в hakaton

# Подключение статических файлов (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Основной маршрут для проверки работы API
@app.get("/")
async def root():
    return {"message": "Hackathon Chat API is running"}

# Запуск приложения через Uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
