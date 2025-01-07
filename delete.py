import os
from pathlib import Path
import argparse
import time

def find_unmatched_images(directory, remove=False):
    start_time = time.time()
    path = Path(directory)
    
    # Get all files in one pass
    image_files = {}
    txt_files = set()
    
    print("Scanning directory...")
    for file in path.iterdir():
        suffix = file.suffix.lower()
        if suffix in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            image_files[file.stem] = file
        elif suffix == '.txt':
            txt_files.add(file.stem)
    
    # Find images without corresponding txt files
    unmatched_images = [image_files[stem] for stem in (image_files.keys() - txt_files)]
    
    print(f"Found {len(unmatched_images)} images without corresponding txt files")
    
    if unmatched_images:
        if remove:
            print(f"Removing {len(unmatched_images)} files...")
            for file in unmatched_images:
                try:
                    file.unlink()
                    print(f"Removed: {file.name}")
                except PermissionError:
                    print(f"Permission denied: Cannot remove {file.name}")
                except Exception as e:
                    print(f"Error removing {file.name}: {e}")
        else:
            for img_file in unmatched_images[:10]:
                print(f"- {img_file.name}")
            if len(unmatched_images) > 10:
                print(f"... and {len(unmatched_images) - 10} more files")
    
    return len(unmatched_images)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find and remove images without matching txt files')
    parser.add_argument('directory', help='Directory containing images and txt files')
    parser.add_argument('--remove', action='store_true', help='Remove unmatched images')
    
    args = parser.parse_args()
    find_unmatched_images(args.directory, args.remove)