from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.conexion_bd import session_dependencia

from app.modelos.facturas import (
    Factura,
    FacturaCrear,
    FacturaEditar,
    FacturaLeer,
)

from app.modelos.clientes import Cliente

rutas_facturas = APIRouter()


@rutas_facturas.get("/Facturas", response_model=list[FacturaLeer])
def listar_facturas(sesion: session_dependencia):

    statement = (
        select(Factura)
        .options(
            selectinload(Factura.cliente),
            selectinload(Factura.transacciones)
        )
    )

    return sesion.exec(statement).all()


@rutas_facturas.get("/Facturas/{factura_id}", response_model=FacturaLeer)
def obtener_factura(factura_id: int, sesion: session_dependencia):

    statement = (
        select(Factura)
        .where(Factura.id == factura_id)
        .options(
            selectinload(Factura.cliente),
            selectinload(Factura.transacciones)
        )
    )

    factura = sesion.exec(statement).first()

    if factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    return factura


@rutas_facturas.post("/Facturas", response_model=FacturaLeer)
def crear_factura(datos: FacturaCrear, sesion: session_dependencia):

    cliente = sesion.get(Cliente, datos.cliente_id)

    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no existe")

    nueva = Factura(
        cliente_id=datos.cliente_id,
        vr_total=datos.vr_total
    )

    sesion.add(nueva)
    sesion.commit()
    sesion.refresh(nueva)

    return nueva


@rutas_facturas.patch("/Facturas/{factura_id}", response_model=FacturaLeer)
def editar_factura(factura_id: int, datos: FacturaEditar, sesion: session_dependencia):

    factura = sesion.get(Factura, factura_id)

    if factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    if datos.cliente_id is not None:

        cliente = sesion.get(Cliente, datos.cliente_id)

        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente no existe")

        factura.cliente_id = datos.cliente_id

    if datos.vr_total is not None:
        factura.vr_total = datos.vr_total

    sesion.add(factura)
    sesion.commit()
    sesion.refresh(factura)

    return factura


@rutas_facturas.delete("/Facturas/{factura_id}")
def eliminar_factura(factura_id: int, sesion: session_dependencia):

    factura = sesion.get(Factura, factura_id)

    if factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    sesion.delete(factura)
    sesion.commit()

    return {"mensaje": "Factura eliminada correctamente"}