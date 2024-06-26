
# SubSearch
<ul>
  <li>An application to upload, parse and store subtitles and query on them</li>
  <li>Developed with AWS - DynamoDB, S3, CloudFront, EC2; Django; CCExtractor; Celery; Redis</li>
  <li>Effectively handles concurrent task executions with Celery and Redis as a broker</li>
</ul>
<img src="https://github.com/pranavs6/subsearch_e/assets/119113218/4e11bb3a-a0d0-4f2b-904e-0efd8a051e67">
<h3>To run the app, follow the steps below</h3>
<ol>
  <li>Clone the project: 'git clone https://github.com/pranavs6/subsearch_e.git'</li>
  <li>Open the project: cd subsearch_e</li>
  <li>Ensure the installation of CCExtractor library on your machine</li>
  <li>Create a new Python virtual environment and enter into the new venv</li>
  <li>Ensure installation of Redis server running on 127.0.0.1:6379</li>
  <li>Install the python libraries by installing the requirements.txt file: 'pip install -r requirements.txt'</li>
  <li>Create a Celery worker: 'celery -A subtitle_project worker -l info --concurrency=4' Change -l (log level) and concurrency to your needs</li>
  <li>Apart from this Celery task, use tmux, open another terminal or use nohup to start Celery and cd into the project again</li>
  <l1>Run the server: 'python manage.py runserver 0.0.0.0:8000</l1>
  <l1>Visit 0.0.0.0:8000 on your web browser</l1>
</ol>
