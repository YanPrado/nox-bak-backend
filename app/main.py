from fastapi import FastAPI

from app.config.settings import settings

app = FastAPI(
    title=settings.APP_NAME
)


@app.get("/")
def root():
    return {
        "message": "NOX BANK API ONLINE 🚀"
    }