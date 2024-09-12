import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db_session
from sqlalchemy import create_engine
from app.api.BUDGET.category_expenses.category_exp_model import CategoryExpenses
from sqlalchemy.orm import sessionmaker
from app.database import Base
from decouple import config

# Cargar las variables de entorno
USERNAME = config('USERNAME_DB')
PASSWORD = config('PASSWORD_DB')
HOST = config('HOST_DB')
PORT = config('PORT_DB')
DB_NAME = config('DATABASE_NAME')

# Configurar la URL de la base de datos para la conexión de prueba
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

# Crear el motor y la sesión de SQLAlchemy
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas de la base de datos para las pruebas
Base.metadata.create_all(bind=engine)

# Sobrescribir la dependencia de la base de datos para usar la sesión de prueba
def override_get_db_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db_session] = override_get_db_session

client = TestClient(app)

# Fixture para gestionar la sesión de la base de datos durante las pruebas
@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fixture para obtener las categorías desde la base de datos
@pytest.fixture
def setup_categories(db_session):
    # Consulta las categorías directamente desde la base de datos
    categories = db_session.query(CategoryExpenses).all()

    return [
        {
            "category_expense_id": category.category_expense_id,
            "category_name": category.category_name,
            "description": category.description
        }
        for category in categories
    ]

# Prueba para obtener todas las categorías
def test_get_all_categories(setup_categories):
    # Prueba para obtener todas las categorías preinsertadas
    response = client.get("/api/categories/")
    assert response.status_code == 200
    data = response.json()["data"]

    # Verifica que se han devuelto las 3 categorías
    assert len(data) == 3

    # Verifica que las categorías preinsertadas están correctas
    for i, category in enumerate(data):
        assert category["category_expense_id"] == setup_categories[i]["category_expense_id"]
        assert category["category_name"] == setup_categories[i]["category_name"]
        assert category["description"] == setup_categories[i]["description"]

# Prueba para obtener una categoría por su ID
def test_get_category_by_id():
    # Prueba para obtener una categoría por su ID
    category_id = 1  # Supongamos que queremos obtener la categoría con ID 1 (Expenses)
    response = client.get(f"/api/categories/{category_id}")
    assert response.status_code == 200

    # Verifica los datos de la categoría con ID 1
    category_data = response.json()["data"]
    assert category_data["category_expense_id"] == 1
    assert category_data["category_name"] == "Expenses"
    assert category_data["description"] == "Fixed and Variable Expenses (e.g., rent, food, transport)"


