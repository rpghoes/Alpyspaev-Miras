import logging
from pythonjsonlogger import jsonlogger
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

# Настройка логгера
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI()

# Метрики Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    logger.info("Health check passed")
    return {"status": "ok"}

@app.get("/test")
def test():
    logger.info("Test endpoint accessed")
    return {"message": "Hello, monitoring!"}
