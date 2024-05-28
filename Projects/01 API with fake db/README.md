# Items API

This is a FastAPI-based project for managing a collection of items. The API allows clients to perform CRUD operations on the items.

The project contains a `test_api.http` file which includes HTTP requests for testing the API. It is designed to be used with the **REST Client** extension in VS Code, providing a convenient way to interact with the API endpoints during development.

## Endpoints

The following endpoints are available in the Items API:

### Get All Items

- **URL:** `/items/all`
- **Method:** `GET`
- **Description:** Retrieves all items in the system.

### Get an Item by ID

- **URL:** `/items/{item_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific item by its ID.
- **Path Parameters:**
  - `item_id` (int): The ID of the item to retrieve.

### Get Items with Query Parameters

- **URL:** `/items/`
- **Method:** `GET`
- **Description:** Retrieves items matching the query parameters.
- **Query Parameters:**
  - `name` (str, optional): The name or partial name of the item.
  - `price` (float, optional): The price of the item.
  - `count` (int, optional): The count of the item in stock.
  - `category` (Category, optional): The category of the item; either `"tools"` or `"consumables"`.

### Add an Item

- **URL:** `/items/`
- **Method:** `POST`
- **Description:** Adds a new item to the system.
- **Request Body:** The item details in JSON format.

### Update an Item

- **URL:** `/items/{item_id}`
- **Method:** `PUT`
- **Description:** Updates an existing item's attributes.
- **Path Parameters:**
  - `item_id` (int): The ID of the item to update.
- **Query Parameters:**
  - `name` (str, optional): The new name of the item (must be 1-8 characters long).
  - `price` (float, optional): The new price of the item (must be greater than 0).
  - `count` (int, optional): The new count of the item (must be greater than 0).

### Delete an Item

- **URL:** `/items/{item_id}`
- **Method:** `DELETE`
- **Description:** Deletes an existing item from the system.
- **Path Parameters:**
  - `item_id` (int): The ID of the item to delete.

## Test API Usage

The `test_api.http` file contains example HTTP requests for testing the API. The file can be used with the REST Client extension in VS Code.
