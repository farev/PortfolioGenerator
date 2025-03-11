#!/bin/bash

# Install alembic if not already installed
pip install alembic

# Initialize alembic
alembic init migrations

# Create a migration script
alembic revision --autogenerate -m "Create initial tables"

# Run the migration
alembic upgrade head 