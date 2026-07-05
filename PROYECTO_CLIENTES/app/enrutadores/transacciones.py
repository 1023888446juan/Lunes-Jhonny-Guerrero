from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.conexion_bd import session_dependencia

from app.modelos.transacciones import (
    Transaccion,
    TransaccionCrear,
    TransaccionEditar,
    TransaccionLeer,
)

from app.modelos.facturas import Factura

rutas_transacciones = APIRouter()


@rutas_transacciones.get("/Transacciones", response_model=list[TransaccionLeer])
def listar_transacciones(sesion: session_dependencia):

    statement = (
        select(Transaccion)
        .options(selectinload(Transaccion.factura))
    )

    return sesion.exec(statement).all()


@rutas_transacciones.get("/Transacciones/{id}", response_model=TransaccionLeer)
def obtener_transaccion(id: int, sesion: session_dependencia):

    statement = (
        select(Transaccion)
        .where(Transaccion.id == id)
        .options(selectinload(Transaccion.factura))
    )

    transaccion = sesion.exec(statement).first()

    if transaccion is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    return transaccion


@rutas_transacciones.post("/Transacciones", response_model=TransaccionLeer)
def crear_transaccion(datos: TransaccionCrear, sesion: session_dependencia):

    factura = sesion.get(Factura, datos.factura_id)

    if factura is None:
        raise HTTPException(status_code=404, detail="La factura no existe")

    nueva = Transaccion(
        cantidad=datos.cantidad,
        vr_unitario=datos.vr_unitario,
        descripcion=datos.descripcion,
        factura_id=datos.factura_id,
    )

    sesion.add(nueva)
    sesion.commit()
    sesion.refresh(nueva)

    return nueva


@rutas_transacciones.patch("/Transacciones/{id}", response_model=TransaccionLeer)
def editar_transaccion(id: int, datos: TransaccionEditar, sesion: session_dependencia):

    transaccion = sesion.get(Transaccion, id)

    if transaccion is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    if datos.factura_id is not None:

        factura = sesion.get(Factura, datos.factura_id)

        if factura is None:
            raise HTTPException(status_code=404, detail="La factura no existe")

        transaccion.factura_id = datos.factura_id

    if datos.cantidad is not None:
        transaccion.cantidad = datos.cantidad

    if datos.vr_unitario is not None:
        transaccion.vr_unitario = datos.vr_unitario

    if datos.descripcion is not None:
        transaccion.descripcion = datos.descripcion

    sesion.add(transaccion)
    sesion.commit()
    sesion.refresh(transaccion)

    return transaccion


@rutas_transacciones.delete("/Transacciones/{id}")
def eliminar_transaccion(id: int, sesion: session_dependencia):

    transaccion = sesion.get(Transaccion, id)

    if transaccion is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    sesion.delete(transaccion)
    sesion.commit()

    return {"mensaje": "Transacción eliminada correctamente"}