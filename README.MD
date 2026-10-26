# Resource Reservation Service

A lightweight FastAPI service for creating, listing, updating, and canceling resource reservations. The current implementation uses in-memory dictionaries for storage and is intended as a starting point for a more production-ready version with a proper database, service layer, and structured models.

## Overview

This service allows you to:
- Create and manage resources such as desks or equipment
- Reserve a resource for a specific time window
- Prevent overlapping bookings for the same resource
- Cancel reservations
- Check the status of resources and reservations

## Current Tech Stack

- Python 3.11
- FastAPI
- Pydantic
- Uvicorn
- Docker / Docker Compose

## Current API Endpoints

The app currently exposes the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Health check |
| POST | /create_resource | Create a new resource |
| GET | /resources/{resource_id} | Fetch a single resource |
| GET | /get-all-resources | List all stored resources |
| DELETE | /delete-resource/{resource_id} | Delete a resource if no active reservation exists |
| POST | /create-reservation | Create a reservation for a resource |
| DELETE | /cancel-reservations/{reservation_id} | Cancel a reservation |
| GET | /list-all-reservations | List all reservations |

### Request and Response Notes

#### Create Resource
Request body:
```json
{
  "name": "Desk 101",
  "type": "desk"
}
```

Response:
```json
{
  "resource_id": "uuid-string",
  "name": "Desk 101",
  "type": "desk",
  "status": "available"
}
```

#### Create Reservation
Request body:
```json
{
  "resource_id": "resource-uuid",
  "user_id": "emp-123",
  "start_time": "2026-10-26T09:00:00",
  "end_time": "2026-10-26T10:00:00"
}
```

Response:
```json
{
  "reservation_id": "uuid-string",
  "resource_id": "resource-uuid",
  "user_id": "emp-123",
  "start_time": "2026-10-26T09:00:00",
  "end_time": "2026-10-26T10:00:00",
  "status": "active"
}
```

## Running the Service Locally

### Option 1: Using Docker Compose
From the project root:
```bash
cd resource-reservation
docker compose up --build
```

This will start the FastAPI app on:
- http://localhost:8000
- Swagger UI: http://localhost:8000/docs

### Option 2: Using Docker directly
```bash
cd resource-reservation
docker build -t resource-reservation .
docker run --rm -p 8000:8000 resource-reservation
```

### Option 3: Running without Docker
```bash
cd resource-reservation
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Project Structure

Current structure:
```text
resource-reservation/
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
├── README.MD
└── tests/
```

## Recommended Next Steps
1. Extract helper functions into helpers.py
2. Move database logic to db.py
3. Create config.py for configuration management

4. Add PUT endpoints for updating resources and reservations
PUT /resources/{resource_id} - Update resource details
PUT /reservations/{reservation_id} - Modify reservation times

5. Add filtering to list endpoints
Filter reservations by user_id, resource_id, status, date_range
Filter resources by type, status

6. Add pagination support
Query parameters: ?skip=0&limit=10

7. The current app stores data in dictionary objects inside the application file. For iteration 2 use actual database

## Production level
1. Idempotency
Use idempotency keys to prevent duplicate requests
Store request hashes

2. Concurrency handling
Implement row-level locking
Handle race conditions for simultaneous bookings

3. Authentication & Authorization
Add JWT tokens
User roles (admin, regular user)
Permission-based access

4. Observability
Add structured logging
Request tracing (correlation IDs)
Metrics (Prometheus)
Health checks with dependency status

## Useful Local URLs

- App root: http://localhost:8000/
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example Commands

```bash
# build and run with Docker Compose
cd resource-reservation
docker compose up --build

# stop containers
cd resource-reservation
docker compose down

# run app directly with uvicorn
cd resource-reservation
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
