from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.interfaces.http.routes import router


def crear_aplicacion() -> FastAPI:
    app = FastAPI(
        title="MiGasto API",
        description="API para gestionar gastos e ingresos personales",
        version="1.0.0",
    )
    app.include_router(router)

    # Archivos estáticos (CSS, JS, etc.)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Interfaz de prueba en la raíz
    @app.get("/", include_in_schema=False)
    def interfaz_prueba():
        return FileResponse("app/static/index.html")

    return app


app = crear_aplicacion()