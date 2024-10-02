
# SubSearch
<ul>
  <li>An application to upload, parse and store subtitles and query on them</li>
  <li>Developed with AWS - DynamoDB, S3, CloudFront, EC2; Django; CCExtractor; Celery; Redis</li>
  <li>Effectively handles concurrent task executions with Celery and Redis as a broker</li>
</ul>
<img src="https://github.com/pranavs6/subsearch_e/assets/119113218/4e11bb3a-a0d0-4f2b-904e-0efd8a051e67">
<h3>To clone and setup stuff</h3>
<ol>
  <li>Clone the project: 'git clone https://github.com/pranavs6/subsearch_e.git'</li>
  <li>Open the project: cd subsearch_e</li>
  <li>Ensure the installation of CCExtractor library on your machine</li>
  <li>Ensure installation of Redis server and that it is running on 127.0.0.1:6379</li>
</ol>
<h3>To run the app with multiple windows to get live logs, follow the steps below</h3>
<ol>
  <li>Create a new Python virtual environment and enter into the new venv</li>
  <li>Install the python libraries by installing the requirements.txt file: 'pip install -r requirements.txt'</li>
  <li>Create a Celery worker: 'celery -A subtitle_project worker -l info --concurrency=4' Change -l (log level) and concurrency to your needs</li>
  <li>Apart from this Celery task, use tmux or open another terminal, cd into the project again</li>
  <li>Run the server: 'python manage.py runserver 0.0.0.0:8000</li>
  <li>Visit 0.0.0.0:8000 on your web browser</li>
</ol>
<h3>To run the app with a single window with log files, follow the steps below</h3>
<ol>
  <li>Setup the project and other dependencies: 'source setup.sh'</li>
  <li>Run the project: 'source run.sh'</li>
  <li>Visit 0.0.0.0:8000 on your web browser</li>
  <li>Kill the project: 'source kill.sh'</li>
</ol>
