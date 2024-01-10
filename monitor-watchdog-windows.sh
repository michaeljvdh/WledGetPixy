#!/bin/bash

# Set the directory to monitor
MONITOR_DIR="/app/monitor"

# Function to be called when a new file is added
on_new_file() {
  echo "New file detected in bash: $1"
  # Add your action here, like triggering the inotify system
  touch $1
}

# Monitor the directory
while true; do
  # Get the list of files currently in the directory
  before=$(ls -1 "$MONITOR_DIR")

  # Wait for a short period before checking again
  sleep 5  # Adjust the sleep duration as needed

  # Get the list of files after the wait
  after=$(ls -1 "$MONITOR_DIR")

  # Compare the before and after to find the new file
  new_files=$(diff <(echo "$before") <(echo "$after") | grep '^>' | cut -d ' ' -f2-)

  # Call the function for each new file
  for file in $new_files; do
    on_new_file "$file"
  done
done
