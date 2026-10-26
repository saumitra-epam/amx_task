## Overview
This project is a small FastAPI-based resource reservation service designed to manage shared resources such as meeting rooms, desks, equipment, or charging slots. It supports creating resources, creating reservations, listing resources and reservations, and cancelling reservations. The application is intentionally lightweight and designed to run locally with Docker Compose so it can be started and tested quickly by another engineer.

## Tradeoffs and design choices

1. In-memory storage was used instead of a database to minimize setup complexity and keep the project focused on the core domain logic.
2. Validation is intentionally basic but useful: the service checks for invalid time ranges and overlapping bookings.
3. Endpoint structure is simple and explicit so the API is easy to inspect, test, and explain.
4. Logging is minimal and practical, aimed at understanding what the service is doing during normal use and failure scenarios.
5. The project avoids advanced infrastructure concerns like authentication, metrics, distributed locks, or full tracing because they are outside the scope of this initial implementation.

## What was intentionally left out

1. Real database persistence
2. Thread-safe or multi-instance concurrency handling
3. Transactional booking guarantees
4. Idempotency enforcement for duplicate client requests
5. Authentication and authorization
6. Role-based access control
7. Pagination and filtering for larger datasets
8. Stronger API versioning and backward compatibility strategy
9. Detailed observability stack, including metrics and distributed tracing
10. Better configuration management and environment separation

## What I would do next with more time

1. Replace in-memory storage with a real database and define clear persistence models.
2. Address race conditions in reservation creation so overlapping bookings are prevented correctly even under concurrent requests.
3. Add proper idempotency handling so retries from clients do not create duplicate reservations.
4. Strengthen the API contract with consistent error responses and clearer validation rules.
5. Add operational tooling such as structured logs, request correlation IDs, health endpoints, and basic metrics.
6. Add more comprehensive automated tests covering invalid inputs, duplicate requests, conflicts, and cancellation behavior.
7. Refine the service design into clear layers such as routes, service logic, and data access, so it is easier to extend safely.