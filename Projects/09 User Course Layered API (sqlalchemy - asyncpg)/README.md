# User Course - Layered API

The API for managing users, courses, sections, and content blocks in an educational platform.

## Project Structure

The project follows a four-level structure for better maintainability and testability:

- **app**: Contains the main application code.
  - **api**: Contains the route handlers/endpoints for the FastAPI application.
  - **crud**: Holds the CRUD (Create, Read, Update, Delete) operations interacting with the database.
  - **schemas**: Contains Pydantic models for request validation and response serialization.
  - **db**: Handles database setup and configurations, including session management and model base classes.

## Features

### General Management

- **User Management**: Handles user registration, authentication, roles, and user status.
- **Course Management**: Facilitates creating and managing courses, including section and content blocks management.

### Authentication & Authorization

- **OAuth2 Authentication**: Implemented using OAuth2, providing secure mechanisms for user sign-up, login, and logout.
- **JWT Tokens**: Authentication utilizes JWT (JSON Web Tokens) for access and refresh tokens, ensuring secure communication.
- **Token Revocation with Redis**: Access and refresh tokens can be revoked using Redis.

### Email Features

- **Email Support with FastAPI-Mail**: Integrated FastAPI-Mail for sending emails.
- **Account Activation**: Implemented account activation via activation emails.
- **Forgot Password**: Users can reset their passwords by receiving a reset email.

## Models

### User

- **id**: Integer, Primary Key, Auto-increment (Unique identifier for the user)
- **email**: String, Unique, Not Null (Email address of the user)
- **role**: Enum (Defines the role of the user such as 'student', 'teacher', etc.)
- **is_active**: Boolean, Default False (Indicates whether the user account is active)

### Course

- **id**: Integer, Primary Key, Auto-increment (Unique identifier for the course)
- **title**: String, Not Null (Title of the course)
- **description**: Text (Description of the course)
- **user_id**: Integer, Foreign Key (Link to the user who created/owns the course)

### StudentCourse

- **id**: Integer, Primary Key, Auto-increment (Unique identifier for the student-course relationship)
- **completed**: Boolean, Default False (Indicates if the student has completed the course)
- **student_id**: Integer, Foreign Key (Link to the student)
- **course_id**: Integer, Foreign Key (Link to the course)

### Section

- **id**: Integer, Primary Key, Auto-increment (Unique identifier for the section)
- **title**: String, Not Null (Title of the section)
- **description**: Text (Description of the section)
- **course_id**: Integer, Foreign Key (Link to the course this section belongs to)

### ContentBlock

- **id**: Integer, Primary Key, Auto-increment (Unique identifier for the content block)
- **title**: String, Not Null (Title of the content block)
- **description**: Text (Description of the content block)
- **type**: Enum (Defines the type of the content block such as 'lesson', 'quiz', etc.)
- **url**: String (URL for content if applicable)
- **content**: Text (Actual content for text-based content blocks)
- **section_id**: Integer, Foreign Key (Link to the section this content block belongs to)

### CompletedContentBlock

- **id**: Integer, Primary Key, Auto-increment (Unique identifier for the completion record)
- **url**: String (URL for any feedback or related content)
- **feedback**: Text (Student's feedback or remarks)
- **grade**: Integer (Grade achieved by the student on this content block)
- **student_id**: Integer, Foreign Key (Link to the student who completed the content block)
- **content_block_id**: Integer, Foreign Key (Link to the content block completed)

## Database Configuration

Rename the `env.txt` file to `.env` and set your database user, password, and database name in the following format:

```
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/mydb"
```

This project uses `PostgreSQL` as the database and `asyncpg` as the dialect/DBAPI for SQLAlchemy.

`asyncpg` is a database interface library designed specifically for `PostgreSQL` and Python/asyncio. `asyncpg` is an efficient, clean implementation of PostgreSQL server binary protocol for use with Python's asyncio framework.

`asyncpg` requires Python 3.8 or later and is supported for `PostgreSQL` versions 9.5 to 16. Older `PostgreSQL` versions or other databases implementing the `PostgreSQL` protocol may work, but are not being actively tested.

## Running Redis

To use Redis for token revocation, you need to have Redis installed and running. You can install and start Redis locally using the following commands:

For Linux:

```sh
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```

For macOS (using Homebrew):

```sh
brew update
brew install redis
brew services start redis
```

For Windows:
Download and install Redis from [Redis Download Page](https://redis.io/download), and start the Redis server by running:

```sh
redis-server
```

Make sure to update your `.env` file with the correct Redis URL:

```
REDIS_URL="redis://localhost:6379/0"
```

This setup ensures Redis is running on `localhost` with the default port `6379`.
