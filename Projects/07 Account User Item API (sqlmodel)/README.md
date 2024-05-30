# Account, Users and Items API

This repository hosts a Python-based web API that allows you to manage data about users and their items. The project leverages [FastAPI](https://fastapi.tiangolo.com/) for creating the API and [SQLModel](https://sqlmodel.tiangolo.com/) for interacting with SQL databases from Python code, with Python data models.

## Features

- **Operations for Account**: Signup, login, logout and reset password for accounts.
- **CRUD Operations for Users**: Create, read, update, and delete users.
- **CRUD Operations for Items**: Create, read, update, and delete items.
- **OAuth2 Authentication**: Secure user authentication using OAuth2 with password flow.

## Models

### User

- `id`: Primary key.
- `email`: Email of the user.
- `password`: Password of the user (hashed).
- `name`: Name of the user.
- `age`: Age of the user.
- `is_active`: Activation status of the user.
- `items`: List of items associated with the user.

### Item

- `id`: Primary key.
- `title`: Title of the item.
- `description`: Description of the item.
- `is_public`: Public status of the item.
- `user_id`: Foreign key linked to the user ID.
- `user`: Relationship to the user of the item.

## Authentication

The API uses OAuth2 with password flow for secure user authentication. Endpoints requiring authentication will expect an OAuth2 token to be provided. You can test this flow using tools such as Postman or the interactive API documentation provided by FastAPI's Swagger UI.

## Testing the API

- Rename the `env.txt` file to `.env` to access the environment variables on your machine.
- Go to the Swagger UI (available at `http://127.0.0.1:8000/docs`) and try to create a new user.
- You can then log in with the created user account to obtain an authentication token and test other endpoints that require authentication.
