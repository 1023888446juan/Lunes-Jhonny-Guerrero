from fastapi import FastAPI

from app.conexion_bd import crear_tablas

from app.enrutadores.clientes import rutas_clientes
from app.enrutadores.facturas import rutas_facturas
from app.enrutadores.transacciones import rutas_transacciones

app = FastAPI(
    title="API Clientes",
    version="1.0.0",
    lifespan=crear_tablas
)

app.include_router(rutas_clientes, tags=["Clientes"])
app.include_router(rutas_facturas, tags=["Facturas"])
app.include_router(rutas_transacciones, tags=["Transacciones"])