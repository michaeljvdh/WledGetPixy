import os
import shutil
import time
import argparse
import configparser

def read_config(config_file, section, option):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config.get(section, option)

def copy_files(source_folder, target_folder, time_interval):
    try:
        files = os.listdir(source_folder)
        if not files:
            print(f"No files found in {source_folder}")
            return

        for filename in files:
            source_file = os.path.join(source_folder, filename)
            target_file = os.path.join(target_folder, filename)

            # Copy the file
            shutil.copy(source_file, target_file)
            print(f"Copied {source_file} to {target_file}")
            
            # Wait for the specified time interval before copying the next file
            time.sleep(time_interval)

    except Exception as e:
        print(f"Error: {str(e)}")

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    config_file = 'monitor.cfg'

    source_folder = read_config(config_file, 'Settings', 'cronpics_location')
    target_folder = read_config(config_file, 'Settings', 'monitor_location')
    ensure_directory_exists(source_folder)

    parser = argparse.ArgumentParser(description="Copy files from one folder to another based on a time interval.")
    parser.add_argument("-time", type=int, required=True, help="Time interval in seconds")
    args = parser.parse_args()

    time_interval = args.time

    while True:
        copy_files(source_folder, target_folder, time_interval)

if __name__ == "__main__":
    main()
