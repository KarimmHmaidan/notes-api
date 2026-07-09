# Notes API

A RESTful Notes API built with FastAPI, PostgreSQL, SQLAlchemy, and Alembic.

## Features

- Create, read, update, and delete notes (CRUD)
- PostgreSQL database integration
- SQLAlchemy ORM
- Pydantic schemas for data validation
- Alembic database migrations
- Clean backend structure using routers and services

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- uv

## Project Structure


app/
├── routers/ # API endpoints
├── schemas/ # Request and response schemas
├── services/ # Business logic
├── models.py # Database models
├── database.py # Database connection
└── main.py # Application entry point

alembic/
└── versions/ # Database migration files


## Setup

Clone the repository:

```bash
git clone https://github.com/KarimmHmaidan/notes-api.git
cd notes-api

Install dependencies:

uv sync

Create a .env file:

DATABASE_URL="put_your_database_url"

Run database migrations:

uv run alembic upgrade head

.start the server 

uv run uvicorn app.main:app --reload

.API documentation:

http://127.0.0.1:8000/docs