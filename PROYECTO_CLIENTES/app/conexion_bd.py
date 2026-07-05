from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///clientes.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)


def get_session():
    with Session(engine) as session:
        yield session


session_dependencia = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def crear_tablas(app):
    SQLModel.metadata.create_all(engine)
    yield