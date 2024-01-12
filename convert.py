import argparse
from PIL import Image
import json
import sys
import configparser
import os


def create_default_config(config_file):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'ipaddress': 'x.x.x.x',
        'brightness': '50',
        'resolution': '16x16'
    }
    with open(config_file, 'w') as f:
        config.write(f)

def read_config(config_file):
    if not os.path.exists(config_file):
        create_default_config(config_file)
    config = configparser.ConfigParser()
    config.read(config_file)
    return (config['DEFAULT']['ipaddress'],
            config['DEFAULT'].getint('brightness'),
            config['DEFAULT']['resolution'])

def write_command_to_file(segment, file_count, ip_address, brightness, output_folder):
    command_data = {"on": True, "bri": brightness, "seg": {"id": 0, "i": segment}}
    command = f'curl -X POST "http://{ip_address}/json/state" -d \'{json.dumps(command_data)}\' -H "Content-Type: application/json"'
    output_path = os.path.join(output_folder, f'{file_count}.send')
    with open(output_path, 'w') as f:
        f.write(command + "\n")


def image_to_wled_commands(image_path, ip_address, resolution, output_folder, brightness):
    MAX_PIXELS_PER_FILE = 500  # Maximum pixels or objects per file
    width, height = map(int, resolution.split('x'))
    total_pixels = width * height

    with Image.open(image_path) as img:
        frame_count = 0
        file_index = 0
        try:
            while True:
                img.seek(frame_count)
                frame = img.convert('RGB')
                frame = frame.resize((width, height))
                pixel_data = []
                last_color = None
                range_start = 0

                for y in range(height):
                    for x in range(width):
                        r, g, b = frame.getpixel((x, y))
                        hex_color = '{:02x}{:02x}{:02x}'.format(r, g, b)
                        index = y * width + x

                        if hex_color != last_color:
                            if last_color is not None:
                                pixel_data.extend([range_start, index, last_color])

                            range_start = index
                            last_color = hex_color

                        # Check if the pixel_data length exceeds the maximum limit
                        if len(pixel_data) >= MAX_PIXELS_PER_FILE * 3:
                            write_segment_to_file(pixel_data, file_index, ip_address, brightness, output_folder, frame_count)
                            file_index += 1
                            pixel_data = []

                # Write remaining data if any
                if last_color is not None:
                    pixel_data.extend([range_start, total_pixels, last_color])
                    write_segment_to_file(pixel_data, file_index, ip_address, brightness, output_folder, frame_count)

                frame_count += 1

        except EOFError:
            # No more frames in the image
            pass

def write_segment_to_file(pixel_data, file_index, ip_address, brightness, output_folder, frame_count):
    command_data = {"on": True, "bri": brightness, "seg": {"id": 0, "i": pixel_data}}
    output_path = os.path.join(output_folder, f'{frame_count}_{file_index}.send')
    with open(output_path, 'w') as f:
        command = f'curl -X POST "http://{ip_address}/json/state" -d \'{json.dumps(command_data, separators=(",", ":"))}\' -H "Content-Type: application/json"'
        f.write(command + "\n")



def main():
    config_ip, config_brightness, resolution = read_config('convert.cfg')

    if config_ip == 'x.x.x.x':
        print("Error: IP address is not configured. Please configure the IP address in convert.cfg.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Convert an image (GIF, PNG, JPG) to WLED curl commands for a serpentine matrix.')
    parser.add_argument('image', help='Path to the input image file (GIF, PNG, JPG).')
    parser.add_argument('output', help='Path to the output file for curl commands.')
    parser.add_argument('--brightness', type=int, default=config_brightness, help='Brightness of the LED matrix (0-255). Use --brightness=value')

    args = parser.parse_args()

    
    image_to_wled_commands(args.image, config_ip, resolution, args.output, args.brightness)

if __name__ == "__main__":
    main()
