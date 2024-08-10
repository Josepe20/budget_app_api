
# Budget API

This is a Backend repository made on top of Python and FastAPI. 

This is a personal project made to showcase my skills with python as backend, is an open source code and  aim of the entire project is to create a "personal finance app" to manage your finance by butgets



## Installation

To run this project execute the following steps

Step 1: Clone the Repository

    git clone ["this repository link"]

Step 2: Create a Virtual Environment

    python -m venv venv

Step 3: Activate a Virtual Environment

on Windows:

    venv\Scripts\activate

on Linux/MacOs:

    source venv/bin/activate

Step 4: Install Dependencies

    pip install -r requirements.txt

Step 5: Run the Application

Move to the app/ directory:
    
    cd app/

Start the FastAPI development server:

    fastapi dev main.py
    
or

    uvicorn main:app --reload

    
## Running Unit Tests

To ensure that everything is working correctly, you can run the unit tests that have been set up.

Run All Tests
To run all the tests:

    pytest tests

Run a Single Test
To run a single test, for example, test_users.py:

    pytest tests/test_users.py


## Evironment Variables

HASHED PASSWORD && JWT SETTINGS

    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

SMTP CREDENTIALS

    SMTP_SERVER=smtp.your_email_provider.com
    SMTP_PORT=587
    SMTP_USERNAME=your_email@example.com
    SMTP_PASSWORD=your_password
    EMAIL_FROM=your_email@example.com
    EMAIL_SUBJECT=Your account needs to be verified

DB CREDENTIALS

    USERNAME_DB=your_username
    PASSWORD_DB=your_password
    HOST_DB=your_host
    PORT_DB=your_port
    DATABASE_NAME=your_db_name

    


## 🚀 About Me
I'm a Python full stack developer... profiency using backend tools such as Django/ FastAPI, SQL and NoSQL Databases and AWS cloud compute.

Frontend skills all related to react ecosystem... React.js,Next.js, React Native, Redux and Zustand. 


