from datetime import datetime
from typing import Optional
from sqlalchemy import Enum as SqlEnum
from app.core.enums import UserStatus

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "auth"}

    role_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    role_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    users: Mapped[list["UserRole"]] = relationship(back_populates="role")
    permissions: Mapped[list["RolePermission"]] = relationship(back_populates="role")


class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema": "auth"}

    permission_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    permission_code: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime)

    roles: Mapped[list["RolePermission"]] = relationship(back_populates="permission")
    users: Mapped[list["UserPermission"]] = relationship(back_populates="permission")


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[UserStatus] = mapped_column(SqlEnum(UserStatus), nullable=False, default=UserStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime)

    roles: Mapped[list["UserRole"]] = relationship(
        back_populates="user",
        foreign_keys="UserRole.user_id",
    )

    extra_permissions: Mapped[list["UserPermission"]] = relationship(
        back_populates="user",
        foreign_keys="UserPermission.user_id",
    )

    granted_permissions: Mapped[list["UserPermission"]] = relationship(
        back_populates="granted_by_user",
        foreign_keys="UserPermission.granted_by",
    )


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = {"schema": "auth"}

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("auth.users.user_id"),
        primary_key=True,
    )

    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("auth.roles.role_id"),
        primary_key=True,
    )

    assigned_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    user: Mapped["User"] = relationship(
        back_populates="roles",
        foreign_keys=[user_id],
    )

    role: Mapped["Role"] = relationship(back_populates="users")


class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = {"schema": "auth"}

    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("auth.roles.role_id"),
        primary_key=True,
    )

    permission_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("auth.permissions.permission_id"),
        primary_key=True,
    )

    assigned_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    role: Mapped["Role"] = relationship(back_populates="permissions")
    permission: Mapped["Permission"] = relationship(back_populates="roles")


class UserPermission(Base):
    __tablename__ = "user_permissions"
    __table_args__ = {"schema": "auth"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("auth.users.user_id"),
        nullable=False,
    )

    permission_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("auth.permissions.permission_id"),
        nullable=False,
    )

    granted_by: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("auth.users.user_id"),
        nullable=True,
    )

    justification: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    user: Mapped["User"] = relationship(
        back_populates="extra_permissions",
        foreign_keys=[user_id],
    )

    permission: Mapped["Permission"] = relationship(back_populates="users")

    granted_by_user: Mapped[Optional["User"]] = relationship(
        back_populates="granted_permissions",
        foreign_keys=[granted_by],
    )