# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 14:44:28 2025

@author: Lucas.Beem
"""

from PIL import Image
from pathlib import Path
from pillow_heif import register_heif_opener
import argparse


# Register the HEIC opener so Pillow can handle HEIC files
register_heif_opener()

def convert_heic_to_jpg(input_path, output_directory=None):
    """
    Converts a HEIC file or all HEIC files in a directory to JPG.

    Args:
        input_path (str or Path): Path to a HEIC file or a directory containing HEIC files.
        output_directory (str or Path, optional): Directory to save the converted JPGs.
                                                 If None, JPGs are saved in the same directory as the HEIC files.
    """
    input_path = Path(input_path)

    if input_path.is_file() and input_path.suffix.lower() in {'.heic', '.heif'}:
        convert_single_file(input_path, output_directory)
    elif input_path.is_dir():
        for heic_file in input_path.rglob("*.[hH][eE][iI][Cc]"):
            convert_single_file(heic_file, output_directory)
    else:
        print(f"Error: Invalid input path or file type: {input_path}")

def convert_single_file(heic_file_path, output_directory):
    try:
        print(f"Converting: {heic_file_path.name}")
        image = Image.open(heic_file_path)
 
        # Ensure the output directory exists
        if output_directory:
            output_dir_path = Path(output_directory)
            output_dir_path.mkdir(parents=True, exist_ok=True)
            new_name = output_dir_path / f"{heic_file_path.stem}.jpg"
        else:
            new_name = heic_file_path.with_suffix('.jpg')
 
        image.convert('RGB').save(new_name)
        print(f"Saved as: {new_name.name}")
    except Exception as e:
        print(f"Error converting {heic_file_path.name}: {e}")
 
if __name__=="__main__":
    
    parser= argparse.ArgumentParser()
    parser.add_argument('input', help="folder that contains the heic to be converted, no trailing slash on path")
    parser.add_argument('output', nargs='?', default= None, help="output folder where the jpg to be saved, if not supplied, input folder used as output folder")
    
    args = parser.parse_args()
    
    print(args)
    
    if args.output == None:
        output = args.input
    else:
        output = args.output
    
    convert_heic_to_jpg(args.input,output_directory=output)
    