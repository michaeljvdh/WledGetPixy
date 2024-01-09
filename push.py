import requests
import re
import argparse
import json
import os
import time

def send_data(json_data, url):
    response = requests.post(url, json=json_data)
    print(response.text)

def extract_json_from_command(command):
    match = re.search(r"-d '(.+?)' -H", command)
    if match:
        json_str = match.group(1)
        return json.loads(json_str)
    else:
        raise ValueError("No JSON data found in the command")

def process_file(file_path, delay):
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                json_data = extract_json_from_command(line)
                url_match = re.search(r"curl -X POST \"(.+?)\"", line)
                if url_match:
                    url = url_match.group(1).replace('/state', '/json')
                    send_data(json_data, url)
                    if delay > 0:
                        time.sleep(delay / 1000.0)
                else:
                    raise ValueError("No URL found in the command")

def main():
    parser = argparse.ArgumentParser(description='Send JSON data to WLED device.')
    parser.add_argument('-folder', '--folder', help='Path to folder containing .send files.')
    parser.add_argument('-file', '--file', help='Specific .send file to process.')
    parser.add_argument('-time', '--time', type=int, default=0, help='Time in milliseconds to wait between sending files.')
    parser.add_argument('-loop', '--loop', type=int, default=1, help='Number of times to loop through sending files.')
    args = parser.parse_args()

    black_json = {"on": True, "bri": 100, "seg": {"id": 0, "i": [0, 256, "000000"]}}

    # Function to extract URL from a .send file
    def extract_url(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                url_match = re.search(r"curl -X POST \"(.+?)\"", line)
                if url_match:
                    return url_match.group(1).replace('/state', '/json')
        return None

    # Extract URL and send the "all black" command
    first_file = args.file if args.file else (sorted(os.listdir(args.folder))[0] if args.folder and os.path.isdir(args.folder) else None)
    if first_file:
        first_file_path = os.path.join(args.folder, first_file) if args.folder else first_file
        url = extract_url(first_file_path)
        if url:
            send_data(black_json, url)
            time.sleep(0)  # Optional delay after sending the "all black" command

    # Rest of the code for iterating through the .send files
    for _ in range(args.loop):
        if args.file:
            process_file(os.path.join(args.folder, args.file), args.time)
        elif args.folder and os.path.isdir(args.folder):
            for file_name in sorted(os.listdir(args.folder)):
                if file_name.endswith('.send'):
                    file_path = os.path.join(args.folder, file_name)
                    print(f"Sending data from file: {file_path}")
                    process_file(file_path, args.time)
        else:
            print("Please specify a valid folder path or file.")
            break

if __name__ == "__main__":
    main()

