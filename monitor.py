import sys
import shutil
import time
import subprocess
import os
import shutil
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

class Watcher:
    def __init__(self, directory_to_watch, config):
        self.observer = Observer()
        self.directory_to_watch = directory_to_watch
        self.config = config

    def run(self):
        event_handler = Handler(self.directory_to_watch, self.config)
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=False)
        self.observer.start()
        print(f"Observer Started: {self.directory_to_watch}")
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, directory_to_watch, config):
        self.directory_to_watch = directory_to_watch
        self.config = config

    def on_any_event(self, event):

        if event.is_directory or 'archive' in event.src_path or 'send' in event.src_path:
            return None

        if event.event_type == 'created':
            print(f"New file detected in python: {event.src_path}")
            send_location = self.config.get('Settings', 'send_location')

            # Process the new file with convert.py
            subprocess.call(["python", "convert.py", event.src_path, send_location])
            
            # Copy each file from folderA to folderB
            shutil.rmtree(send_data_archive_location)
            os.makedirs(send_data_archive_location, exist_ok=True)
            for filename in os.listdir(send_location):
                file_path = os.path.join(send_location, filename)
                if os.path.isfile(file_path):
                    shutil.copy(file_path, send_data_archive_location)

            # Send all .send files from send_location
            self.send_data(send_location)

            # Cleanup the send folder
            self.cleanup_send_folder(send_location)

            # Move and delete operations
            if self.config.getboolean('Settings', 'move_to_archive'):
                self.move_to_archive(event.src_path)
            # Delete images from monitor folder after processing.
            self.delete_file(event.src_path)

    def send_data(self, send_folder):        
        subprocess.call(["python", "push.py", "-folder", send_folder])

    def cleanup_send_folder(self, send_location):        
        print("Cleaning up send folder...")
        for file in os.listdir(send_location):
            file_path = os.path.join(send_location, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print(f"Deleted file: {file_path}")

    def move_to_archive(self, file_path):
        archive_path = self.config.get('Settings', 'archive_location')
        shutil.copy(file_path, archive_path)
        print(f"Copied to archive: {file_path}")

    def delete_file(self, file_path):
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('monitor.cfg')

    directory_to_watch = config.get('Settings', 'monitor_location')
    archive_location = config.get('Settings', 'archive_location')
    send_location = config.get('Settings', 'send_location')
    send_data_archive_location = config.get('Settings', 'send_data_archive_location')
    directory_to_watch = os.path.abspath(directory_to_watch)

    # Ensure directories exist
    ensure_directory_exists(directory_to_watch)
    ensure_directory_exists(archive_location)
    ensure_directory_exists(send_location)
    ensure_directory_exists(send_data_archive_location)

    w = Watcher(directory_to_watch, config)
    w.run()
