from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.conexion_bd import session_dependencia

from app.modelos.clientes import (
    Cliente,
    ClienteCrear,
    ClienteEditar,
    ClienteLeer,
)

rutas_clientes = APIRouter()


@rutas_clientes.get("/clientes", response_model=list[ClienteLeer])
def listar_clientes(sesion: session_dependencia):

    statement = (
        select(Cliente)
        .options(selectinload(Cliente.facturas))
    )

    return sesion.exec(statement).all()


@rutas_clientes.get("/clientes/{cliente_id}", response_model=ClienteLeer)
def obtener_cliente(cliente_id: int, sesion: session_dependencia):

    statement = (
        select(Cliente)
        .where(Cliente.id == cliente_id)
        .options(selectinload(Cliente.facturas))
    )

    cliente = sesion.exec(statement).first()

    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return cliente


@rutas_clientes.post("/clientes", response_model=ClienteLeer)
def crear_cliente(datos: ClienteCrear, sesion: session_dependencia):

    cliente = Cliente.model_validate(datos)

    sesion.add(cliente)
    sesion.commit()
    sesion.refresh(cliente)

    return cliente


@rutas_clientes.patch("/clientes/{cliente_id}", response_model=ClienteLeer)
def editar_cliente(cliente_id: int, datos: ClienteEditar, sesion: session_dependencia):

    cliente = sesion.get(Cliente, cliente_id)

    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    cambios = datos.model_dump(exclude_unset=True)

    for campo, valor in cambios.items():
        setattr(cliente, campo, valor)

    sesion.add(cliente)
    sesion.commit()
    sesion.refresh(cliente)

    return cliente


@rutas_clientes.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, sesion: session_dependencia):

    cliente = sesion.get(Cliente, cliente_id)

    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    sesion.delete(cliente)
    sesion.commit()

    return {"mensaje": "Cliente eliminado correctamente"}