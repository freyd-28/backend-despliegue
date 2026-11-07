
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base


# Leer variables del entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_SSL_CA = os.getenv("DB_SSL_CA")


# Validar configuración
variables = {
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_NAME": DB_NAME,
    "DB_SSL_CA": DB_SSL_CA,
}

faltantes = [
    nombre for nombre, valor in variables.items()
    if not valor
]

if faltantes:
    raise RuntimeError(
        f"Faltan variables de conexión: {', '.join(faltantes)}"
    )

if not os.path.isfile(DB_SSL_CA):
    raise FileNotFoundError(
        f"No se encontró el certificado SSL: {DB_SSL_CA}"
    )


# Construir conexión
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
    query={"charset": "utf8mb4"},
)


# Conexión segura con Aiven
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {"ca": DB_SSL_CA},
        "connect_timeout": 30
    },
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_timeout=30,
)


# Sesiones y modelos
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

Base = declarative_base()
Base.metadata.bind = engine

__all__ = ["engine", "session", "Base"]



