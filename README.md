
# Project Demo: Using Openhands - AI-Powered Coding Solution - with $1,5 Using Anthropic APIs

## Command Prompt
- Implement a microservice for saving user Firebase token or APNS token for push notifications in Python.
- Try to implement it using a database with good performance in production.
- Give me the Dockerfile
- Can you give me the unittest and BDD?

=====================================================================================

# Push Notification Token Service

A microservice for managing push notification tokens (FCM and APNS) with PostgreSQL backend and comprehensive test coverage.

## Features

- Token registration for FCM and APNS
- Token retrieval by user ID
- Token deletion
- Duplicate token prevention
- Async API with FastAPI
- PostgreSQL database with async support
- Docker support
- Comprehensive test suite (Unit tests and BDD)

## Prerequisites

- Python 3.12+
- PostgreSQL 15+
- Docker and Docker Compose (optional)

## Installation

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/HuyNguyenDinh/openhands-demo.git
cd push_notification_service
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies using Poetry:
```bash
pip install poetry
poetry install
```

4. Set up PostgreSQL:
```bash
# Create database
createdb -h localhost -U postgres push_notifications

# Set password for postgres user (if not already set)
psql -h localhost -U postgres
ALTER USER postgres PASSWORD 'postgres';
\q
```

5. Create .env file:
```bash
echo "DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/push_notifications" > .env
```

6. Run database migrations:
```bash
alembic upgrade head
```

### Docker Setup

1. Build and start the services:
```bash
docker-compose up --build
```

The service will be available at http://localhost:8000.

## API Documentation

After starting the service, visit http://localhost:8000/docs for the interactive API documentation.

### API Endpoints

1. Register a token:
```bash
curl -X POST http://localhost:8000/api/v1/tokens \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "token": "fcm_token_xyz",
    "platform": "fcm"
  }'
```

2. Get user tokens:
```bash
curl http://localhost:8000/api/v1/tokens/user123
```

3. Delete a token:
```bash
curl -X DELETE http://localhost:8000/api/v1/tokens/token_uuid_here
```

## Testing

The project includes both unit tests and BDD (Behavior-Driven Development) tests.

### Running Tests

1. Create test database:
```bash
createdb -h localhost -U postgres push_notifications_test
```

2. Run all tests:
```bash
./run_tests.sh
```

Or run specific test types:

```bash
# Run only unit tests with coverage
pytest

# Run only BDD tests
behave
```

### Test Structure

- `tests/unit/`: Unit tests using pytest
- `tests/integration/`: Integration tests
- `features/`: BDD tests using behave
  - `features/*.feature`: Feature specifications in Gherkin syntax
  - `features/steps/`: Step definitions
  - `features/environment.py`: Test environment setup

## Project Structure

```
push_notification_service/
├── alembic/                  # Database migrations
├── app/
│   ├── api/                 # API endpoints
│   ├── database/           # Database configuration
│   ├── models/             # SQLAlchemy models
│   └── schemas/            # Pydantic schemas
├── features/               # BDD tests
│   ├── steps/             # Step definitions
│   └── environment.py     # Test environment setup
├── tests/
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── .env                  # Environment variables
├── .gitignore           # Git ignore file
├── alembic.ini          # Alembic configuration
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile          # Docker configuration
├── pyproject.toml     # Poetry dependencies
└── README.md         # Project documentation
```

## Development

### Adding New Features

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and write tests
3. Run the test suite
4. Create a pull request

### Database Migrations

To create a new migration:
```bash
alembic revision --autogenerate -m "description of changes"
```

To apply migrations:
```bash
alembic upgrade head
```

## Production Deployment

1. Update environment variables:
   - Set secure database credentials
   - Configure appropriate host and port
   - Set production-specific settings

2. Build and deploy using Docker:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Monitoring and Maintenance

- The service includes health checks for both the application and database
- PostgreSQL connection pooling is configured for optimal performance
- Database indexes are set up for efficient queries
- Logs are available in the container logs

## Contributing

1. Fork the repository
2. Create your feature branch
3. Write tests for your changes
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
