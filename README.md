# MiGasto API

Backend para gestionar gastos e ingresos personales, desarrollado con **Python, FastAPI, SQLAlchemy y SQLite en memoria**.

## Inicio rápido (desde cualquier computador)

Estos comandos te permiten instalar, ejecutar y probar el proyecto en cualquier máquina con Python, sin afectar instalaciones globales.

### 1. Obtener el proyecto
Descarga o clona la carpeta del proyecto y entrágala:
```powershell
cd ruta\del\proyecto
```

### 2. Crear el entorno virtual
```powershell
python -m venv .venv
```

### 3. Instalar las dependencias
Con el entorno activado:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si PowerShell bloquea la activación, usa directamente el intérprete de `.venv` (sin cambiar la política de ejecución del sistema):
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Ejecutar la API
Con el entorno activado:
```powershell
uvicorn app.main:app --reload
```

O directamente con el intérprete de `.venv`:
```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### 5. Probar la aplicación
Abre tu navegador en:
- http://127.0.0.1:8000/ → **Interfaz sencilla para crear, listar, eliminar movimientos y ver el balance**
- http://127.0.0.1:8000/docs → Documentación automática (Swagger)

### 6. Detener la API
Presiona `Ctrl+C` en la terminal donde esté corriendo uvicorn.

Para eliminar el proyecto por completo, basta con borrar la carpeta del proyecto (el entorno virtual está contenido en ella).

---

## Arquitectura

El proyecto sigue una arquitectura desacoplada inspirada en los principios y convenciones de Scaffold Bancolombia, adaptada a Python y FastAPI:

- **Domain**: entidades de dominio independientes de frameworks (`app/domain`).
- **Contracts**: interfaces (contratos) de persistencia (`app/contracts`).
- **Application**: casos de uso que dependen de contratos, no de implementaciones (`app/application`).
- **Infrastructure / Persistence**: adaptadores SQLAlchemy, DBOs, mapeadores y repositorio concreto (`app/infrastructure`).
- **Interfaces HTTP**: esquemas Pydantic y rutas FastAPI (`app/interfaces/http`).

## Estructura de carpetas

```
migasto/
├── .venv/                     # Entorno virtual (excluido de git)
├── .gitignore
├── requirements.txt
├── README.md
└── app/
    ├── main.py                # Punto de entrada FastAPI
    ├── config/
    │   └── database.py        # Engine SQLAlchemy y sesión (SQLite en memoria)
    ├── domain/
    │   ├── models.py          # Movimiento (entidad de dominio), TipoMovimiento
    │   └── exceptions.py
    ├── contracts/
    │   └── repositories.py    # IMovimientoRepository (contrato)
    ├── application/
    │   ├── dtos.py
    │   └── use_cases/
    │       ├── crear_movimiento.py
    │       ├── obtener_movimiento.py
    │       ├── listar_movimientos.py
    │       ├── actualizar_movimiento.py
    │       ├── eliminar_movimiento.py
    │       └── calcular_balance.py
    ├── infrastructure/
    │   └── persistence/
    │       ├── dbo/
    │       │   └── movimiento_dbo.py   # Modelo DBO de SQLAlchemy
    │       ├── mappers.py              # MovimientoMapper (dominio <-> DBO)
    │       └── repository.py           # SQLAlchemyMovimientoRepository
    └── interfaces/
        └── http/
            ├── schemas.py    # Esquemas Pydantic
            └── routes.py     # Rutas FastAPI
```

## Entorno virtual y dependencias (Windows PowerShell)

Todas las operaciones se realizan con el intérprete de Python del entorno virtual `.venv`, **sin tocar instalaciones globales**.

### 1. Crear el entorno virtual

```powershell
python -m venv .venv
```

### 2. Activar el entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación por la directiva de ejecución, no modifiques la política del sistema. Usa directamente el ejecutable de Python dentro de `.venv`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### 3. Instalar dependencias

Con el entorno activado:

```powershell
pip install -r requirements.txt
```

O, sin activar (usando directamente el intérprete de `.venv`):

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Desactivar el entorno virtual

Solo si lo activaste normalmente con `Activate.ps1`:

```powershell
deactivate
```

## Ejecutar la API

Desde la carpeta raíz del proyecto, con el entorno virtual activado:

```powershell
uvicorn app.main:app --reload
```

O sin activar el entorno, llamando directamente al intérprete de `.venv`:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

La API quedará disponible en:

- http://127.0.0.1:8000
- Documentación automática (Swagger): http://127.0.0.1:8000/docs
- Documentación alternativa (ReDoc): http://127.0.0.1:8000/redoc

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/movimientos` | Crear un movimiento (gasto o ingreso) |
| GET | `/movimientos/{id}` | Obtener un movimiento por ID |
| GET | `/movimientos` | Listar todos los movimientos |
| PUT | `/movimientos/{id}` | Actualizar un movimiento |
| DELETE | `/movimientos/{id}` | Eliminar un movimiento |
| GET | `/balance` | Consultar balance (ingresos, gastos, saldo neto) |

## Ejemplo de cuerpo de solicitud (POST /movimientos)

```json
{
  "descripcion": "Salario mensual",
  "monto": 1500.00,
  "tipo": "INGRESO",
  "categoria": "Trabajo",
  "fecha": "2026-10-15T08:00:00"
}
```

## Notas técnicas

- **SQLite en memoria**: la base de datos se crea en memoria mediante SQLAlchemy con `StaticPool`, manteniéndose disponible durante la ejecución de la aplicación.
- **Decimal**: los importes monetarios se manejan con `Decimal` para evitar errores de punto flotante. Se almacenan con `Numeric` de SQLAlchemy, compatible con SQLite.
- **Sin autenticación ni pruebas automatizadas**: fuera del alcance definido para este proyecto.

## Eliminar el proyecto

Como todo está contenido en la carpeta del proyecto y el entorno virtual está en `.venv/`, basta con eliminar la carpeta del proyecto para desinstalarlo por completo, sin afectar otros proyectos ni las dependencias globales de Python.