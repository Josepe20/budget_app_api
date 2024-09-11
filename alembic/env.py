# alembic/env.py
import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from decouple import config as decouple_config

# Añadir la ruta del proyecto al path de Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

# Importa tu modelo Base aquí
from app.database import Base  # Asegúrate de que esta ruta es correcta
from api.AUTH.users import user_model  # Importa todos los modelos necesarios

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# Obtén las variables de entorno usando decouple
USERNAME = decouple_config('USERNAME_DB')
PASSWORD = decouple_config('PASSWORD_DB')
HOST = decouple_config('HOST_DB')
PORT = decouple_config('PORT_DB')
DB_NAME = decouple_config('DATABASE_NAME')

DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

# Establecer sqlalchemy.url en el objeto de configuración
config.set_main_option('sqlalchemy.url', DATABASE_URL)

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
