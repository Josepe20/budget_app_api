# Usa la imagen oficial de Python 3.10
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requirements y configuraciones necesarias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Dar permisos al entrypoint
RUN chmod +x ./bin/entrypoint.sh

# Exponer el puerto 8000 para FastAPI
EXPOSE 8000

# Definir el entrypoint
ENTRYPOINT ["./bin/entrypoint.sh"]
