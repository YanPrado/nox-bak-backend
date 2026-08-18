import hashlib
import secrets

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.repositories import (
    PermissionRepository,
    ProfileRepository,
    UserRepository,
)


class AccessService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.permissions = PermissionRepository(db)
        self.profiles = ProfileRepository(db)
        self.users = UserRepository(db)

    @staticmethod
    def _required(obj, message: str):
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        return obj

    @staticmethod
    def _hash_password(password: str) -> str:
        iterations = 600_000
        salt = secrets.token_hex(16)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            bytes.fromhex(salt),
            iterations,
        ).hex()

        return f"pbkdf2_sha256${iterations}${salt}${password_hash}"

    async def _get_permissions(
        self,
        permission_ids: list[int],
    ):
        if not permission_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O perfil deve possuir ao menos uma permissão.",
            )

        permissions = await self.permissions.get_many(permission_ids)

        if len(permissions) != len(set(permission_ids)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Uma ou mais permissões não foram encontradas.",
            )

        return permissions

    # =========================================================
    # PERMISSÕES
    # =========================================================

    async def list_permissions(
        self,
        name: str | None = None,
    ):
        return await self.permissions.list_all(name)

    async def get_permission(
        self,
        permission_id: int,
    ):
        permission = await self.permissions.get(permission_id)

        return self._required(
            permission,
            "Permissão não encontrada.",
        )

    async def create_permission(
        self,
        data: dict,
    ):
        permission = await self.permissions.create(data)

        await self.db.commit()
        await self.db.refresh(permission)

        return permission

    async def update_permission(
        self,
        permission_id: int,
        data: dict,
    ):
        permission = await self.get_permission(permission_id)

        await self.permissions.update(permission, data)
        await self.db.commit()
        await self.db.refresh(permission)

        return permission

    async def delete_permission(
        self,
        permission_id: int,
    ):
        permission = await self.get_permission(permission_id)

        await self.permissions.delete(permission)
        await self.db.commit()

    # =========================================================
    # PERFIS
    # =========================================================

    async def list_profiles(
        self,
        name: str | None = None,
    ):
        return await self.profiles.list_all(name)

    async def get_profile(
        self,
        profile_id: int,
    ):
        profile = await self.profiles.get(profile_id)

        return self._required(
            profile,
            "Perfil não encontrado.",
        )

    async def create_profile(
        self,
        data: dict,
    ):
        permission_ids = data.pop("permission_ids")

        await self._get_permissions(permission_ids)

        profile = await self.profiles.create(data)

        await self.profiles.set_permissions(
            profile.role_id,
            permission_ids,
        )

        await self.db.commit()

        return await self.profiles.get(profile.role_id)

    async def update_profile(
        self,
        profile_id: int,
        data: dict,
    ):
        profile = await self.get_profile(profile_id)
        permission_ids = data.pop("permission_ids", None)

        if permission_ids is not None:
            await self._get_permissions(permission_ids)

            await self.profiles.set_permissions(
                profile_id,
                permission_ids,
            )

        await self.profiles.update(profile, data)
        await self.db.commit()

        return await self.profiles.get(profile_id)

    async def delete_profile(
        self,
        profile_id: int,
    ):
        profile = await self.get_profile(profile_id)

        if await self.profiles.has_users(profile_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="O perfil possui usuários vinculados.",
            )

        await self.profiles.delete_with_permissions(profile)
        await self.db.commit()

    # =========================================================
    # USUÁRIOS
    # =========================================================

    async def list_users(self):
        return await self.users.list_all()

    async def get_user(
        self,
        identifier: str,
    ):
        user = await self.users.get_by_id(identifier)

        return self._required(
            user,
            "Usuário não encontrado.",
        )

    async def create_user(
        self,
        data: dict,
    ):
        role_id = data.pop("role_id")
        password = data.pop("password")

        await self.get_profile(role_id)

        user = await self.users.create(
            {
                **data,
                "password_hash": self._hash_password(password),
            }
        )

        await self.users.set_role(
            user.user_id,
            role_id,
        )

        await self.db.commit()

        return await self.users.get_by_id(str(user.user_id))

    async def update_user(
        self,
        user_id: int,
        data: dict,
    ):
        user = await self.users.get(user_id)

        self._required(
            user,
            "Usuário não encontrado.",
        )

        role_id = data.pop("role_id", None)
        password = data.pop("password", None)

        if role_id is not None:
            await self.get_profile(role_id)

        if password is not None:
            data["password_hash"] = self._hash_password(password)

        await self.users.update(user, data)

        if role_id is not None:
            await self.users.set_role(
                user_id,
                role_id,
            )

        await self.db.commit()

        return await self.users.get_by_id(str(user_id))

    async def delete_user(
        self,
        user_id: int,
    ):
        user = await self.users.get(user_id)

        self._required(
            user,
            "Usuário não encontrado.",
        )

        await self.users.delete_with_relations(user)
        await self.db.commit()