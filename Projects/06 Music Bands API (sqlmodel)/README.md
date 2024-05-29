# Music Bands API

This repository hosts a Python-based web API that allows you to manage data about music bands and their albums. The project leverages [FastAPI](https://fastapi.tiangolo.com/) for creating the API and [SQLModel](https://sqlmodel.tiangolo.com/) for interacting with an SQLite database.

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

## Project Structure

- **app/**: Contains the core source code for the application.

  - `db.py`: Handles database initialization and session management. Responsible for creating the SQLite database and providing session management for database operations.
  - `main.py`: Implements API endpoints and app configuration. It defines the FastAPI app and includes all the route handlers for the various API endpoints.
  - `models.py`: Defines SQLModel models and Pydantic schemas. Contains the data models for `Band` and `Album`, including the relationships between them.
  - `populate.py`: Populates the database with initial data. It initializes the database and inserts predefined band and album data.

- **test_api.http**: Provides HTTP requests for testing the API. This file contains sample requests to interact with the API endpoints and requires the REST Client extension in VS Code to execute.

## Testing the API

The `api.http` file includes several pre-configured HTTP requests that can be used to test the various endpoints of the API. You can use the REST Client extension in VS Code to execute these requests. If you want, you can run the `python app/populate.py` command to initialize the database with some example data.