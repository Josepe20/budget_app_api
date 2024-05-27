from fastapi import FastAPI
from app.router import index as router_index

app = FastAPI()

# Incluir el router principal
app.include_router(router_index.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to My Budget App"}
