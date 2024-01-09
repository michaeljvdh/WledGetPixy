import sys
from PIL import Image

def resize_image(input_path, output_path, resolution):
    try:
        with Image.open(input_path) as img:            
            img = img.convert('RGB')            
            width, height = map(int, resolution.split('x'))            
            resized_img = img.resize((width, height), Image.NEAREST)
            resized_img.save(output_path)

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    if len(sys.argv) != 4:
        print("Usage: img.py <input_image> <resolution> <output_image>")
        sys.exit(1)

    input_image = sys.argv[1]
    resolution = sys.argv[2]
    output_image = sys.argv[3]

    resize_image(input_image, output_image, resolution)

if __name__ == "__main__":
    main()
