from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class TransaccionBase(SQLModel):
    cantidad: int
    vr_unitario: float
    descripcion: str


class TransaccionCrear(TransaccionBase):
    factura_id: int


class TransaccionEditar(SQLModel):
    cantidad: Optional[int] = None
    vr_unitario: Optional[float] = None
    descripcion: Optional[str] = None
    factura_id: Optional[int] = None


class TransaccionLeer(TransaccionBase):
    id: int
    factura_id: int

    class Config:
        from_attributes = True


class Transaccion(TransaccionBase, table=True):
    __tablename__ = "transaccion"

    id: Optional[int] = Field(default=None, primary_key=True)

    factura_id: int = Field(foreign_key="factura.id")

    factura: Optional["Factura"] = Relationship(back_populates="transacciones")


from app.modelos.facturas import Factura