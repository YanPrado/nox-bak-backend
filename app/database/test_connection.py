import asyncio

from sqlalchemy import text

from app.database.session import AsyncSessionLocal


async def test_database_connection() -> None:
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                text("SELECT current_database(), current_user;")
            )

            row = result.one()

            print("Conexão com PostgreSQL bem-sucedida!")
            print(f"Database: {row[0]}")
            print(f"User: {row[1]}")

    except Exception as error:
        print("Erro ao conectar no PostgreSQL:")
        print(error)


if __name__ == "__main__":
    asyncio.run(test_database_connection())