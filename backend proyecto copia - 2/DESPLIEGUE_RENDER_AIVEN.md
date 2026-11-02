# Despliegue de BilleterAPP en Aiven + Render

## Cambios incluidos
- `run.py`: lee `FLASK_CONFIG` desde variables de entorno.
- `src/models/__init__.py`: lee `DATABASE_URL` y permite configurar TLS con `DB_SSL_CA`.
- `src/__init__.py`: CORS configurable mediante `CORS_ORIGINS`.
- `requirements.txt`: dependencias para Render.
- `.gitignore`: evita subir `.env`, entornos virtuales y archivos temporales.

## Render
Si `run.py` esta en la raiz del repositorio:
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn run:app`

Si el backend esta dentro de una subcarpeta del repositorio, configurar esa carpeta en Render > Root Directory.

## Variables de entorno en Render
- `FLASK_CONFIG` = `production`
- `DEBUG` = `False`
- `SECRET_KEY` = una clave aleatoria larga
- `JWT_SECRET_KEY` = otra clave aleatoria larga
- `DATABASE_URL` = `mysql+pymysql://USUARIO:CONTRASENA@HOST:PUERTO/BASE?charset=utf8mb4`
- `DB_SSL_CA` = `/etc/secrets/ca.pem`
- `CORS_ORIGINS` = `*` (solo si la API sera consumida por app movil / cliente publico y no se usan cookies; preferible restringirlo al dominio del frontend web cuando exista)

En Render > Environment > Secret Files, crear un archivo llamado `ca.pem` y pegar el contenido del certificado CA descargado desde Aiven. No subir el certificado ni credenciales a GitHub.

## Importante sobre DATABASE_URL
Reemplazar los valores de ejemplo por los datos reales de Aiven. El usuario y la contrasena deben estar correctamente codificados para URL si contienen caracteres especiales. La base de datos debe existir y el archivo SQL debe haberse importado antes de iniciar la API.

## Nota
`Base.metadata.create_all(engine)` crea tablas faltantes segun los modelos, pero no migra automaticamente cambios de columnas ni importa los registros de la base local.
