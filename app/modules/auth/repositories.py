import re
from typing import Generic, TypeVar

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.auth.models import (
    Permission,
    Role,
    RolePermission,
    User,
    UserRole,
)


Model = TypeVar("Model")


class BaseRepository(Generic[Model]):

    def __init__(self, db: AsyncSession, model: type[Model]):
        self.db = db
        self.model = model

    async def get(self, object_id: int) -> Model | None:
        return await self.db.get(self.model, object_id)

    async def list_all(self) -> list[Model]:
        result = await self.db.execute(select(self.model))
        return list(result.scalars().all())

    async def create(self, data: dict) -> Model:
        obj = self.model(**data)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(self, obj: Model, data: dict) -> Model:
        for field, value in data.items():
            setattr(obj, field, value)

        await self.db.flush()
        return obj

    async def delete(self, obj: Model) -> None:
        await self.db.delete(obj)


class PermissionRepository(BaseRepository[Permission]):

    def __init__(self, db: AsyncSession):
        super().__init__(db, Permission)

    async def list_all(
        self,
        name: str | None = None,
    ) -> list[Permission]:

        stmt = select(Permission).order_by(
            Permission.permission_code
        )

        if name:
            stmt = stmt.where(
                Permission.permission_code.ilike(f"%{name}%")
            )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_many(
        self,
        permission_ids: list[int],
    ) -> list[Permission]:

        result = await self.db.execute(
            select(Permission).where(
                Permission.permission_id.in_(permission_ids)
            )
        )

        return list(result.scalars().all())


class ProfileRepository(BaseRepository[Role]):
    """
    O sistema chama de perfil, mas no banco o model é Role.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db, Role)

    async def get(self, role_id: int) -> Role | None:
        result = await self.db.execute(
            select(Role)
            .options(
                selectinload(Role.permissions)
                .selectinload(RolePermission.permission)
            )
            .where(Role.role_id == role_id)
        )

        return result.scalar_one_or_none()

    async def list_all(
            self,
            name: str | None = None,
        ) -> list[Role]:

        stmt = (
            select(Role)
            .options(
                selectinload(Role.permissions)
                .selectinload(RolePermission.permission)
            )
            .order_by(Role.role_name)
        )

        if name:
            stmt = stmt.where(
                Role.role_name.ilike(f"%{name}%")
            )

        result = await self.db.execute(stmt)
        return list(result.scalars().unique().all())

    async def has_users(self, role_id: int) -> bool:
        result = await self.db.execute(
            select(UserRole.user_id)
            .where(UserRole.role_id == role_id)
            .limit(1)
        )

        return result.scalar_one_or_none() is not None


class UserRepository(BaseRepository[User]):

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def list_all(self) -> list[User]:
        result = await self.db.execute(
            select(User)
            .options(
                selectinload(User.roles)
                .selectinload(UserRole.role)
            )
            .order_by(User.full_name)
        )

        return list(result.scalars().unique().all())

    async def get_by_id(
        self,
        identifier: str,
    ) -> User | None:
        """
        Pesquisa pelo mesmo endpoint usando:
        - ID;
        - CPF;
        - nome.
        """

        identifier = identifier.strip()
        cpf = re.sub(r"\D", "", identifier)

        filters = [
            User.full_name.ilike(f"%{identifier}%")
        ]

        if identifier.isdigit():
            filters.append(User.user_id == int(identifier))

        if len(cpf) == 11:
            filters.append(User.cpf == cpf)

        result = await self.db.execute(
            select(User)
            .options(
                selectinload(User.roles)
                .selectinload(UserRole.role)
            )
            .where(or_(*filters))
            .order_by(
                (
                    func.lower(User.full_name)
                    == identifier.lower()
                ).desc(),
                User.full_name,
            )
        )

        return result.scalars().first()