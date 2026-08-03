from fastapi import APIRouter

from app.modules.auth.controller import router as auth_router


api_router = APIRouter()

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Controle de acesso"],
)