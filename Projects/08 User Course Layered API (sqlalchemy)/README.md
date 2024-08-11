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

- **User Management**: Handles user registration, authentication, roles, and user status.
- **Course Management**: Facilitates creating and managing courses, including section and content blocks management.


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
DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/mydb"
```

This project uses PostgreSQL as the database and `psycopg2` as the dialect for SQLAlchemy.

We use `Alembic` for database migrations to manage schema changes.

Run the following command to initialize the tables in the database:

```bash
cd app
alembic upgrade head
```

This will apply all the migrations and set up the initial database schema.
