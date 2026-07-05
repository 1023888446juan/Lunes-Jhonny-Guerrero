from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class ClienteBase(SQLModel):
    nombre: str
    correo: str
    descripcion: str


class ClienteCrear(ClienteBase):
    pass


class ClienteEditar(SQLModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    descripcion: Optional[str] = None


class ClienteLeer(ClienteBase):
    id: int

    class Config:
        from_attributes = True


class Cliente(ClienteBase, table=True):
    __tablename__ = "cliente"

    id: Optional[int] = Field(default=None, primary_key=True)

    facturas: list["Factura"] = Relationship(back_populates="cliente")


from app.modelos.facturas import Factura