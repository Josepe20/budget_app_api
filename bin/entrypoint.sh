#!/bin/bash

# Correr migraciones de Alembic antes de iniciar la aplicación
alembic upgrade head

# Iniciar FastAPI
exec cd app/
exec fastapi main.py --host 0.0.0.0 --port 8000
