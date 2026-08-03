from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.modules.auth.schemas import (
    PermissionCreate,
    PermissionResponse,
    PermissionUpdate,
    RoleCreate,
    RoleResponse,
    RoleUpdate,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.modules.auth.services import AccessService


router = APIRouter()


def get_service(
    db: AsyncSession = Depends(get_db),
) -> AccessService:
    return AccessService(db)


# =========================================================
# PERMISSÕES
# =========================================================

@router.post(
    "/permissions",
    response_model=PermissionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_permission(
    data: PermissionCreate,
    service: AccessService = Depends(get_service),
):
    return await service.create_permission(data.model_dump())


@router.get(
    "/permissions",
    response_model=list[PermissionResponse],
)
async def list_permissions(
    name: str | None = Query(default=None),
    service: AccessService = Depends(get_service),
):
    return await service.list_permissions(name)


@router.get(
    "/permissions/{permission_id}",
    response_model=PermissionResponse,
)
async def get_permission(
    permission_id: int,
    service: AccessService = Depends(get_service),
):
    return await service.get_permission(permission_id)


@router.patch(
    "/permissions/{permission_id}",
    response_model=PermissionResponse,
)
async def update_permission(
    permission_id: int,
    data: PermissionUpdate,
    service: AccessService = Depends(get_service),
):
    return await service.update_permission(
        permission_id,
        data.model_dump(exclude_unset=True),
    )


@router.delete(
    "/permissions/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_permission(
    permission_id: int,
    service: AccessService = Depends(get_service),
):
    await service.delete_permission(permission_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# =========================================================
# PERFIS
# =========================================================

@router.post(
    "/profiles",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    data: RoleCreate,
    service: AccessService = Depends(get_service),
):
    return await service.create_profile(data.model_dump())


@router.get(
    "/profiles",
    response_model=list[RoleResponse],
)
async def list_profiles(
    name: str | None = Query(default=None),
    service: AccessService = Depends(get_service),
):
    return await service.list_profiles(name)


@router.get(
    "/profiles/{profile_id}",
    response_model=RoleResponse,
)
async def get_profile(
    profile_id: int,
    service: AccessService = Depends(get_service),
):
    return await service.get_profile(profile_id)


@router.patch(
    "/profiles/{profile_id}",
    response_model=RoleResponse,
)
async def update_profile(
    profile_id: int,
    data: RoleUpdate,
    service: AccessService = Depends(get_service),
):
    return await service.update_profile(
        profile_id,
        data.model_dump(exclude_unset=True),
    )


@router.delete(
    "/profiles/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_profile(
    profile_id: int,
    service: AccessService = Depends(get_service),
):
    await service.delete_profile(profile_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# =========================================================
# USUÁRIOS
# =========================================================

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: UserCreate,
    service: AccessService = Depends(get_service),
):
    return await service.create_user(data.model_dump())


@router.get(
    "/users",
    response_model=list[UserResponse],
)
async def list_users(
    service: AccessService = Depends(get_service),
):
    return await service.list_users()


@router.get(
    "/users/{identifier}",
    response_model=UserResponse,
)
async def get_user(
    identifier: str,
    service: AccessService = Depends(get_service),
):
    return await service.get_user(identifier)


@router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
)
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: AccessService = Depends(get_service),
):
    return await service.update_user(
        user_id,
        data.model_dump(exclude_unset=True),
    )


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    service: AccessService = Depends(get_service),
):
    await service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)