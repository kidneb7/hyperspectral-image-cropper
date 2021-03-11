import spectral
import spectral.io.envi as envi
import cv2

import numpy as np 
import matplotlib.pyplot as plt

import os 
import argparse
import pathlib

def select_roi(input_path, output_path, output_path_rgb, rgb_bands):
    img = envi.open(input_path)
    
    # Make RGB image
    spectral.save_rgb(
        output_path_rgb,
        img,
        bands=rgb_bands
    )
    
    # Select ROI with cv2
    im = cv2.imread(output_path_rgb)
    from_center = False # We use this variable for parameter clarification in cv2.selectROI()
    r = cv2.selectROI(
        "Image",
        im,
        from_center
    )

    # Crop datacube with ROI
    img_subset = img.read_subimage(rows=range(r[1], r[1]+r[3]), cols=range(r[0], r[0]+r[2]))
    envi.save_image(
        output_path,
        img_subset,
        force=True # Overwrites already existing file
    )
    print("Successfully cropped hyperspectral datacube to", output_path, "cropped at", r)

    # Crop RGB with ROI
    output_path_rgb = output_path[:-3] + 'png'
    cropped_rgb = im[r[1]:r[1]+r[3], r[0]:r[0]+r[2]]
    cv2.imwrite(output_path_rgb, cropped_rgb)
    print("Successfully cropped RGB to", output_path_rgb, "cropped at", r)


def crop_single(input_path, output_path, output_path_rgb, rgb_bands):
    select_roi(
        input_path,
        output_path,
        output_path_rgb,
        rgb_bands
    )

def crop_multi(input_path, output_path, output_path_rgb, rgb_bands):
    while(True):
        print("Specify output filename (\"cancel\" to exit ROI selection):")
        output_filename = input()
        output_path = 'data/output/' + output_filename + '.hdr'
        if output_filename == 'cancel':
            break
        select_roi(
            input_path,
            output_path,
            output_path_rgb,
            rgb_bands
        )


def main(args):
    INPUTPATH = args.filename
    OUTPUTPATH = 'data/output/cropped.hdr'
    OUTPUT_RGB = 'data/output/RGB.png'

    RGBBANDS = [10, 20, 30]

    if args.multi:
        crop_multi(
            INPUTPATH,
            OUTPUTPATH,
            OUTPUT_RGB,
            RGBBANDS
        )
    else:
        crop_single(
            INPUTPATH,
            OUTPUTPATH,
            OUTPUT_RGB,
            RGBBANDS)
    pass

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Hyperspectral Image Cropper')
    parser.add_argument(
        "-f",
        dest="filename",
        required=True,
        metavar="FILE",
        help="path to input file",
        type=str,
    )
    
    parser.add_argument(
        '-m',
        '--multi',
        action='store_true',
        help='activate multiple crops on the same image'
    )

    args = parser.parse_args()

    output_dir = pathlib.Path('data/output')
    output_dir.mkdir(exist_ok=True, parents=True)

    main(args)