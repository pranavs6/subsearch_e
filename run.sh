git pull
source venv/bin/activate
nohup celery -A subtitle_project worker -l info --concurrency=4 > celery_output.log 2>&1 &
nohup python manage.py runserver 0.0.0.0:8000 > server_output.log 2>&1 &

