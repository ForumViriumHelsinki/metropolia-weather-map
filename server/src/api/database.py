import os

from sqlmodel import Session, SQLModel, create_engine

DB_NAME = os.environ.get("DB_NAME", "weatherdb")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "pass")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)


def get_session():
	with Session(engine) as session:
		yield session
