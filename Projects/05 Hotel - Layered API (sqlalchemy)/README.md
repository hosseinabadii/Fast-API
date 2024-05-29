# Hotel Management System - Layered API

The API for managing hotel operations, including handling customers, rooms, and bookings.

## Project Structure

The project follows a three-level structure for better maintainability and testability:

- **app**: Contains the main application code.
    - **db**: Handles the database operations.
    - **operations**: Implements the business logic for managing customers, rooms, and bookings.
    - **routers**: Defines the API routes for accessing the functionality.

## Features

- **Customer Management**: View, add, update, and delete customer records.
- **Room Management**: Manage room details such as number, size, and pricing.
- **Booking Management**: Facilitate the booking process and maintain reservation records.

## Models

### Customer

- **id**: Primary key.
- **first_name**: First Name of the customer.
- **last_name**: Last Name of the customer.
- **email_address**: Email address of the customer.

### Room

- **id**: Primary key.
- **number**: Number of the room.
- **size**: Size of the room.
- **price**: Price of the room.

### Booking

- **id**: Primary key.
- **from_date**: Starting date of the booking (YYYY-MM-DD).
- **to_date**: Ending date of the booking (YYYY-MM-DD).
- **price**: Total price for the booking.
- **customer_id**: Foreign key linked to the customer ID.
- **room_id**: Foreign key linked to the room ID.
- **customer**: Relationship to the customer who booked the room.
- **room**: Relationship to the room that the customer has booked.
