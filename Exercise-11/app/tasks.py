import time
from app.celery_app import celery

@celery.task
def send_email(email: str):
    print(f"📨 Sending email to {email}")
    time.sleep(5)
    print(f"✅ Email sent to {email}")
    return f"Email to {email} sent successfully"
