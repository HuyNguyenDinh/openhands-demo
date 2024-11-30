#!/bin/bash

# Create test database
PGPASSWORD=postgres createdb -h localhost -U postgres push_notifications_test

# Run unit tests with coverage
echo "Running unit tests..."
pytest

# Run BDD tests
echo "Running BDD tests..."
behave

# Drop test database
PGPASSWORD=postgres dropdb -h localhost -U postgres push_notifications_test