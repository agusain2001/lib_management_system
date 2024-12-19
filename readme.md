# Library Management System - Flask API

## Project Overview
This Flask-based API allows for managing a Library System with functionality for books and members. The API supports CRUD operations, user authentication, and secure password management.

---

## How to Run the Project

### Prerequisites
1. Python 3.7 or later installed on your system.
2. Ensure `pip` is installed and updated (`pip install --upgrade pip`).
3. Clone the repository or copy the project files.

### Installation Steps
1. Navigate to the project directory:
    ```bash
    cd library-management-system
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Initialize the database:
    ```bash
    python -c "from app import db; db.create_all()"
    ```

5. Run the Flask application:
    ```bash
    python app.py
    ```

6. The API will be available at `http://127.0.0.1:5000/`.

---

## Design Choices

1. **Framework**:
   - Flask was chosen for its simplicity, flexibility, and robust extensions like SQLAlchemy, Marshmallow, and JWT-Extended.

2. **Database**:
   - SQLite is used for simplicity and ease of setup for this assignment.

3. **Authentication**:
   - JWT-based token authentication ensures secure access to protected routes, enabling future scalability.

4. **Data Modeling**:
   - Two models, `Book` and `Member`, handle core functionalities, with clear separation of concerns and extendability.

5. **Password Security**:
   - Passwords are hashed using `Flask-Bcrypt` to ensure security.

6. **Serialization**:
   - Marshmallow is used to serialize/deserialize database objects to/from JSON.

7. **RESTful API**:
   - Follows REST principles for predictable and consistent endpoints.

---

## Assumptions and Limitations

### Assumptions:
1. All books have a title and author, and these are mandatory fields.
2. Members must provide a unique email and password to register.
3. Pagination and search functionalities can be added as enhancements in the future.

### Limitations:
1. **Database**: The SQLite database is used for simplicity but may not scale well for production use. Consider PostgreSQL or MySQL for larger deployments.
2. **Validation**: Basic validation is implemented. Additional checks (e.g., title length, email format) could be added.
3. **Error Handling**: Limited error handling; edge cases may need custom error messages and logging.
4. **No Frontend**: This is a backend-only implementation.

---

## Example Endpoints

### Books
- **Create Book**: `POST /books`
- **Get Book**: `GET /books/<book_id>`
- **Get All Books**: `GET /books`
- **Update Book**: `PUT /books/<book_id>`
- **Delete Book**: `DELETE /books/<book_id>`

### Members
- **Create Member**: `POST /members`
- **Login**: `POST /login`
- **Get All Members (Protected)**: `GET /members`

---

## Testing

1. Use a tool like `Postman` or `cURL` to test the API endpoints.
2. Example of creating a book using `cURL`:
    ```bash
    curl -X POST http://127.0.0.1:5000/books -H "Content-Type: application/json" -d '{"title": "Example Book", "author": "John Doe"}'
    ```

---

## Future Enhancements
1. Add pagination for `GET` endpoints.
2. Implement advanced search functionality for books by title or author.
3. Add role-based access control for members.
4. Improve error handling and validation.

