from fastapi import FastAPI
from router import index as router_index
#from database import engine, Base

# Crear todas las tablas en la base de datos (solo para desarrollo)
#Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir el router principal
app.include_router(router_index.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to My Budget App"}
