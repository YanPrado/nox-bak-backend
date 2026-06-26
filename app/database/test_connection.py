from sqlalchemy import text
from app.database.session import SessionLocal

def test_database_connection():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT current_database(), current_user;"))
        row = result.fetchone()
        print("Conexao com PostgreSql - Bem sucedida!")
        print(f"Database: {row[0]}, User: {row[1]}")
        print(f"User: {row[1]}")

    except Exception as error:
        print("Erro ao conectar no PostgreSQL")
        print(error)

    finally:
        db.close()


if __name__ == "__main__":
    test_database_connection()