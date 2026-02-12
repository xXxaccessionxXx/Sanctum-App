from PIL import Image
import os
import sys

# Ensure pillow is installed (it usually is, or included in many envs)
try:
    from PIL import Image
except ImportError:
    print("Error: Pillow library not found. Please run 'pip install Pillow'")
    sys.exit(1)

def create_ico(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        return

    try:
        img = Image.open(input_path)
        # Sizes for standard Windows icons
        icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        img.save(output_path, sizes=icon_sizes)
        print(f"Successfully created icon: {output_path}")
    except Exception as e:
        print(f"Error creating icon: {e}")

if __name__ == "__main__":
    # Default paths relative to project root
    input_file = "assets/icon.png"
    output_file = "assets/icon.ico"
    
    # Allow arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    create_ico(input_file, output_file)
