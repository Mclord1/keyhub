#!/bin/bash

set -e

git restore .
git pull origin dev
echo "Successfully fetched repository updates"

# Install any new dependencies
source venv/bin/activate
pip install -r requirements.txt

# Find all running application processes
worker_pids=$(ps aux | grep 'gunicorn -b' | grep -v grep | awk '{print $2}')

# Start up new workers
echo "Spawning workers"
nohup gunicorn -b 0.0.0.0:5000 -w 2 app:app >> /home/ubuntu/logs 2>&1 < /dev/null &

# Kill the old worker processes
echo "Killing old processes"

for pid in "$worker_pids"; do
  kill -TERM $pid
done

echo "Application udpate has been completed"

