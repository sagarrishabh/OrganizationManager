# Organization Manager

## Overview

The Organization Manager is a robust system for managing organizations, providing functionality for user authentication, organization database management, and administrative operations. This application is built using FastAPI and utilizes SQLite as its database. Dependency management is handled using Poetry, and the application includes a Docker file for containerized deployments.

## Features

- **User Authentication**: Secure login and session management.
- **Organization Management**: Create and read organizations.
- **Database Operations**: Automated handling of organization-specific data.
- **Administrative Tools**: Features for managing organization admins.

## Requirements

- Python 3.12+
- SQLite
- [Poetry](https://python-poetry.org/)

## Installation

1. **Create and activate a virtual environment:**

   For Python 3.12, you can create a virtual environment using:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

2. **Install Poetry**:
   
   Follow the installation guide from the [official Poetry website](https://python-poetry.org/docs/#installation) to set up Poetry on your environment.

    OR 
    
    Install using this command: 
    ```bash
    pip install poetry
    ```
   Disable poetry's virtual env creation since we already created a virtual environment in the last step.
   ```bash
   poetry config virtualenvs.create false
   ```
   
3. **Install dependencies:**

   With Poetry installed, navigate to your project directory and run:
   ```bash
   poetry install
   ```

4. **Configure environment variables:**

   Create a `.env` file in the root of the project with any necessary configuration variables(optional):
   ```
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   SECRET_KEY=your_secret_key
   ```

## Usage

1. **Initialize the SQLite database:**

   Use Alembic to run database migrations:
   ```bash
   alembic upgrade head
   ```

2. **Start the FastAPI server:**

   Use the following command to start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

   By default, the application will be accessible at [http://localhost:8000](http://localhost:8000).


3. **API Documentation:**

   Access interactive API documentation at:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Docker

A Dockerfile is available for building a containerized version of the application. You can build and run the image using these commands:

1. **Build the Docker image:**

   ```bash
   docker build -t organization-manager .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -p 8000:8000 organization-manager
   ```

## Contact

For questions or feedback, please contact [sagarrishabh68@gmail.com](mailto:sagarrishabh68@gmail.com).