"""
Módulo: Auth
Arquivo: schemas.py

Responsabilidade:
    Definir os contratos de entrada e saída da API para autenticação,
    usuários, perfis, permissões e permissões excepcionais.

Este arquivo pode:
    - Validar dados recebidos pela API.
    - Definir campos retornados nas respostas.
    - Normalizar campos simples, como CPF.
    - Ocultar campos sensíveis, como password_hash.

Este arquivo NÃO pode:
    - Consultar banco de dados.
    - Aplicar regras de negócio que dependam do banco.
    - Gerar JWT.
    - Gerar hash de senha.
    - Registrar auditoria ou eventos XES.
"""

import re
from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

from app.core.enums.user_status import UserStatus


def normalize_cpf(value: str) -> str:
    cpf = re.sub(r"\D", "", value)

    if len(cpf) != 11:
        raise ValueError("O CPF deve possuir 11 dígitos.")

    return cpf


# =========================================================
# PERMISSÕES
# =========================================================

class PermissionBase(BaseModel):
    permission_code: str = Field(
        min_length=2,
        max_length=100,
    )
    description: Optional[str] = Field(
        default=None,
        max_length=255,
    )


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    permission_code: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    description: Optional[str] = Field(
        default=None,
        max_length=255,
    )


class PermissionResponse(PermissionBase):
    permission_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# RELACIONAMENTO PERFIL X PERMISSÃO
# =========================================================

class RolePermissionCreate(BaseModel):
    role_id: int = Field(gt=0)
    permission_id: int = Field(gt=0)


class RolePermissionResponse(RolePermissionCreate):
    assigned_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# PERFIS
# =========================================================

class RoleBase(BaseModel):
    role_name: str = Field(
        min_length=2,
        max_length=100,
    )
    description: Optional[str] = Field(
        default=None,
        max_length=255,
    )


class RoleCreate(RoleBase):
    permission_ids: list[int] = Field(
        min_length=1,
        description="O perfil deve possuir pelo menos uma permissão.",
    )


class RoleUpdate(BaseModel):
    role_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    description: Optional[str] = Field(
        default=None,
        max_length=255,
    )
    permission_ids: Optional[list[int]] = Field(
        default=None,
        min_length=1,
        description="O perfil não pode ficar sem permissões.",
    )


class RoleResponse(RoleBase):
    role_id: int
    created_at: datetime
    permissions: list[RolePermissionResponse] = Field(
        default_factory=list
    )

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# RELACIONAMENTO USUÁRIO X PERFIL
# =========================================================

class UserRoleCreate(BaseModel):
    user_id: int = Field(gt=0)
    role_id: int = Field(gt=0)


class UserRoleResponse(UserRoleCreate):
    assigned_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# PERMISSÕES EXCEPCIONAIS DO USUÁRIO
# =========================================================

class UserPermissionCreate(BaseModel):
    user_id: int = Field(gt=0)
    permission_id: int = Field(gt=0)
    granted_by: Optional[int] = Field(default=None, gt=0)
    justification: Optional[str] = None
    active: bool = True
    expires_at: Optional[datetime] = None


class UserPermissionUpdate(BaseModel):
    active: Optional[bool] = None
    justification: Optional[str] = None
    expires_at: Optional[datetime] = None


class UserPermissionResponse(UserPermissionCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# USUÁRIOS
# =========================================================

class UserBase(BaseModel):
    full_name: str = Field(
        min_length=3,
        max_length=255,
    )
    cpf: str
    email: EmailStr
    status: UserStatus = UserStatus.ACTIVE

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, value: str) -> str:
        return normalize_cpf(value)


class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=128,
    )
    role_id: int = Field(
        gt=0,
        description="Perfil obrigatório do usuário.",
    )


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=255,
    )
    cpf: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[UserStatus] = None
    password: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=128,
    )
    role_id: Optional[int] = Field(
        default=None,
        gt=0,
    )

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        return normalize_cpf(value)


class UserResponse(BaseModel):
    user_id: int
    full_name: str
    cpf: str
    email: EmailStr
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    roles: list[UserRoleResponse] = Field(
        default_factory=list
    )

    extra_permissions: list[UserPermissionResponse] = Field(
        default_factory=list
    )

    model_config = ConfigDict(from_attributes=True)