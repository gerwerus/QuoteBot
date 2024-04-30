#!/bin/bash

alembic revision --autogenerate -m "Initial"
alembic upgrade head

gunicorn webapp.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
