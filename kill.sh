#!/bin/bash

echo "Stopping Django server..."
django_pid=$(ps aux | grep 'manage.py runserver' | grep -v grep | awk '{print $2}')
if [ -n "$django_pid" ]; then
    kill $django_pid
    echo "Django server stopped."
else
    echo "Django server not running."
fi

echo "Stopping Celery worker..."
celery_pid=$(ps aux | grep 'celery worker' | grep -v grep | awk '{print $2}')
if [ -n "$celery_pid" ]; then
    kill $celery_pid
    echo "Celery worker stopped."
else
    echo "Celery worker not running."
fi

if [ -f "venv/bin/activate" ]; then
    echo "Deactivating virtual environment..."
    deactivate
else
    echo "Virtual environment not found."
fi

echo "All processes terminated and virtual environment deactivated."

