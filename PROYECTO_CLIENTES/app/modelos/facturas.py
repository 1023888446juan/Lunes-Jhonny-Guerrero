from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class FacturaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)
    vr_total: float


class FacturaCrear(SQLModel):
    cliente_id: int
    vr_total: float


class FacturaEditar(SQLModel):
    cliente_id: Optional[int] = None
    vr_total: Optional[float] = None


class FacturaLeer(FacturaBase):
    id: int
    cliente_id: int

    class Config:
        from_attributes = True


class Factura(FacturaBase, table=True):
    __tablename__ = "factura"

    id: Optional[int] = Field(default=None, primary_key=True)

    cliente_id: int = Field(foreign_key="cliente.id")

    cliente: Optional["Cliente"] = Relationship(back_populates="facturas")

    transacciones: list["Transaccion"] = Relationship(back_populates="factura")


from app.modelos.clientes import Cliente
from app.modelos.transacciones import Transaccion