from fastapi import FastAPI
from app.tasks import send_email

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI + Celery running"}

@app.post("/send-email/")
def trigger_email(email: str):
    send_email.delay(email)
    return {"message": f"Email to {email} is being sent in background"}
