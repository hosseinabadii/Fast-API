# Hotel Management System - Layered API

The API for managing hotel operations, including handling customers, rooms, and bookings.

## Project Structure

The project follows a three-level structure for better maintainability and testability:

- **hotel**: Contains the main application code.
- **db**: Handles the database operations.
- **operations**: Implements the business logic for managing customers, rooms, and bookings.
- **routers**: Defines the API routes for accessing the functionality.

## Features

- **Customer Management**: View, add, update, and delete customer records.
- **Room Management**: Manage room details such as number, size, and pricing.
- **Booking Management**: Facilitate the booking process and maintain reservation records.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.10+
- pip

### Installation

1. Clone the repository

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Start the FastAPI server:
```bash
uvicorn main:app --reload
```
The `--reload` flag enables hot reloading during development.

4. Open your web browser and go to `http://localhost:8000` for the FastAPI documentation.

## Usage

Explain how to use the system, including creating, viewing, updating, and deleting records for customers, rooms, and bookings.

## License

This project is licensed under the [MIT License](./LICENSE).
