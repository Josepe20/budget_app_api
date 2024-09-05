from fastapi import FastAPI
from app.router import index as router_index
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.auth_middleware import AuthMiddleware

app = FastAPI()

origins = [
    "http://localhost:8081",
    "http://127.0.0.1:8081",
    # Añadir otros orígenes si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)


# Incluir el router principal
app.include_router(router_index.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to My Budget App"}
