import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# En Render, DATABASE_URL contiene la cadena de conexion de Aiven.
# En local se conserva una conexion MySQL local como respaldo.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root@localhost:3306/billeterapp_base_datos?charset=utf8mb4"
)

# Si DB_SSL_CA esta definida, PyMySQL verifica la conexion usando el
# certificado CA cargado como archivo secreto en Render.
ssl_ca = os.getenv("DB_SSL_CA")
connect_args = {"ssl": {"ca": ssl_ca}} if ssl_ca else {}

engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True,
    connect_args=connect_args,
)

session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

Base = declarative_base()
Base.metadata.bind = engine

__all__ = ["engine", "session", "Base"]
