from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

# URL de la base de datos SQLite en memoria (se pierde al cerrar la aplicación)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Engine de SQLAlchemy configurado para SQLite en memoria
# check_same_thread=False permite usar la conexión en distintos hilos (necesario para FastAPI)
# StaticPool mantiene un único pool de conexión para que la BD en memoria persista
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Fábrica de sesiones de SQLAlchemy (no hace commit ni flush automático)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos DBO (Data Base Objects) declarativos
Base = declarative_base()


# Generador de sesiones de base de datos (dependencia de FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()