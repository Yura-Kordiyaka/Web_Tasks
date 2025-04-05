
# Django API Test

## Overview

This project is a test API built with Django. It provides endpoints for performing basic operations on tasks and managing users, including authentication.

## Running the Application

To start the application go to the **app** folder and write the command : ` docker-compose up --build`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected routes, include the token in the `Authorization` header with the `Bearer` scheme.


## Security

- **JWT Authentication:** Include the JWT token in the `Authorization` header with the `Bearer` scheme.

## Swagger
- **Swagger UI:** You can access the Swagger UI for API documentation and testing at [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/).