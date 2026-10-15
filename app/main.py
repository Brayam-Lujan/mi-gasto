from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.interfaces.http.routes import router


def crear_aplicacion() -> FastAPI:
    # Crea la instancia de FastAPI con metadatos de la API
    app = FastAPI(
        title="MiGasto API",
        description="API para gestionar gastos e ingresos personales",
        version="1.0.0",
    )
    # Registra las rutas HTTP definidas en routes.py
    app.include_router(router)

    # Sirve archivos estáticos (CSS, JS) desde la carpeta app/static en la ruta /static
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Ruta raíz: devuelve la interfaz HTML de prueba al acceder a http://127.0.0.1:8000/
    @app.get("/", include_in_schema=False)
    def interfaz_prueba():
        return FileResponse("app/static/index.html")

    return app


# Instancia de la aplicación que Uvicorn ejecutará
app = crear_aplicacion()