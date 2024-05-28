# Fast API

This repository contains projects and examples demonstrating the usage of FastAPI, SQLAlchemy, and SQLModel in Python.

## Introduction

[FastAPI](https://fastapi.tiangolo.com/) is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. It is designed to be easy to use and intuitive, while also being highly efficient and scalable.

[SQLAlchemy](https://www.sqlalchemy.org/) is a powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python. It provides a set of high-level API for working with relational databases, allowing you to interact with databases using Python objects and SQL expressions.

[SQLModel](https://sqlmodel.tiangolo.com/) is a library for interacting with SQL databases from Python code, with Python data models. It's inspired by SQLAlchemy and Pydantic, leveraging their strengths to provide a simpler and more efficient way to work with databases.

This repository aims to provide practical examples and projects that demonstrate how to leverage the capabilities of FastAPI, SQLAlchemy, and SQLModel to build robust and efficient web APIs with database integration.

## Features

- Integration of FastAPI with SQLAlchemy and SQLModel for database operations
- CRUD (Create, Read, Update, Delete) operations using FastAPI, SQLAlchemy, and SQLModel
- Authentication and authorization using FastAPI security features
- Data validation and request/response models with Pydantic and SQLModel
- Simplified database interactions with SQLModel's intuitive and type-safe API

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.11+
- pip

## Installation

To set up the project, follow these steps:

1. **Clone the repository:**

   ```shell
   git clone https://github.com/hosseinabadii/Fast-API.git
   cd Fast-API
   ```

2. **Create and activate a virtual environment:**

   ```shell
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies:**

   ```shell
   pip install -r requirements.txt
   ```

## Usage

1. Navigate to the project you want, for example:

   ```shell
   cd "01 API with fake db"
   ```

2. Run the FastAPI application in development mode:

   ```shell
   fastapi dev app/main.py
   ```

   The application will be available at `http://127.0.0.1:8000/`.

3. Access the automatic interactive API documentation (Swagger UI):

   Open your web browser and go to `http://127.0.0.1:8000/docs`. This will display the Swagger UI, where you can interact with the API endpoints directly from the browser.

   You can also access the alternative ReDoc documentation at `http://127.0.0.1:8000/redoc`.

## License

This project is licensed under the MIT [License](LICENSE). Feel free to customize and modify the above template according to your specific project requirements.
