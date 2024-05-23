# Bands API powered by FastAPI

Welcome to the Bands API project! This repository hosts a Python-based web API that allows you to manage data about music bands and their albums. The project leverages [FastAPI](https://fastapi.tiangolo.com/) for creating the API and [SQLModel](https://sqlmodel.tiangolo.com/) for interacting with an SQLite database.

## Features

- **CRUD Operations for Bands**: Create, read, and list bands.
- **Query Bands by Genre**: Filter bands by music genre.
- **Albums Management**: Associate albums with bands and manage their data.
- **Search Bands by Name**: Perform search queries on band names.

## Models

### Band

- `id`: Primary key.
- `name`: Name of the band.
- `genre`: Genre of the band (Rock, Electronic, Shoegaze, Hip-Hop).
- `albums`: List of albums associated with the band.

### Album

- `id`: Primary key.
- `title`: Title of the album.
- `release_date`: Release date of the album.
- `band_id`: Foreign key linked to the band.

## Endpoints

### `GET /`

Returns a welcome message.

### `GET /bands`

Returns a list of all bands. Supports optional query parameters `genre` (to filter by genre) and `q` (to search by band name).

### `GET /bands/{band_id}`

Returns details of a specific band by ID.

### `GET /bands/genre/{genre}`

Returns a list of bands filtered by genre.

### `POST /bands`

Creates a new band. Allows optional inclusion of albums in the request body.

## Project Structure

- **src/**: Contains the core source code for the application.

  - `db.py`: Handles database initialization and session management. Responsible for creating the SQLite database and providing session management for database operations.
  - `main.py`: Implements API endpoints and app configuration. It defines the FastAPI app and includes all the route handlers for the various API endpoints.
  - `models.py`: Defines SQLModel models and Pydantic schemas. Contains the data models for `Band` and `Album`, including the relationships between them.
  - `populate.py`: Populates the database with initial data. It initializes the database and inserts predefined band and album data.

- **api.http**: Provides HTTP requests for testing the API. This file contains sample requests to interact with the API endpoints and requires the REST Client extension in VS Code to execute.

- **db.sqlite**: The SQLite database file that stores the application's data.

- **README.md**: This file, providing comprehensive documentation about the project.

- **requirements.txt**: Lists the required Python packages. Lists all the Python dependencies that need to be installed to run the project.

## Setup & Installation

To get this project up and running on your local machine:

1. **Prerequisites**

   Ensure you have Python 3.11+ and pip installed on your machine. You can check your Python version by running:

   ```sh
   python --version
   ```

2. **Change directory to the project, create a Virtual Environment**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Initialize the Database**

   Before running the application, initialize the database by running:

   ```sh
   python src/populate.py
   ```

5. **Run the Application**

   ```sh
   fastapi dev src/main.py
   ```

   The application will be available at `http://127.0.0.1:8000/`.

## Testing the API

The `api.http` file includes several pre-configured HTTP requests that can be used to test the various endpoints of the API. You can use the REST Client extension in VS Code to execute these requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
