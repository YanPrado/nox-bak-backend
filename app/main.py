from fastapi import FastAPI

from app.router import api_router


app = FastAPI(
    title="NOX Bank API",
    version="1.0.0",
)

app.include_router(
    api_router,
    prefix="/api/v1",
)


@app.get("/health", tags=["Sistema"])
async def health_check():
    return {"status": "online"}