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

    return input_path, output_path, output_path_rgb, rgb_bands, r

def crop_and_save(input_path, output_path, output_path_rgb, rgb_bands, r):
    img = envi.open(input_path)
    # Crop datacube with ROI
    img_subset = img.read_subimage(rows=range(r[1], r[1]+r[3]), cols=range(r[0], r[0]+r[2]))
    envi.save_image(
        output_path,
        img_subset,
        force=True # Overwrites already existing file
    )
    print("Successfully cropped hyperspectral datacube to", output_path, "cropped at", r)

    # Crop RGB with ROI
    im = cv2.imread(output_path_rgb)
    output_path_rgb = output_path[:-3] + 'png'
    cropped_rgb = im[r[1]:r[1]+r[3], r[0]:r[0]+r[2]]
    cv2.imwrite(output_path_rgb, cropped_rgb)
    print("Successfully cropped RGB to", output_path_rgb, "cropped at", r)
    


def specific_aspect_ratio(args, r):
    print("Crop r:\t\t\t {}".format(r))
    aspect_ratio = args.aspect_ratio / 100
    tolerance = 0.01 # parameter to control output assertion

    r0 = r[0]
    r1 = r[1]
    r2 = r[2]
    r3 = r[3]
    
    c1 = r3 # Height of crop in y direction
    c2 = r2 # Width of crop in x direction

    # From crop height (c1), calculate desired width (c3) for correct AR
    c3 = int(np.floor(
        c1 * aspect_ratio
    ))

    # If crop width is big enough, we're finished since we can make a crop of desired aspect ratio within
    # the original crop. However, if it isn't we need to calculate a need constraint on the height (c4)
    # based on available crop width (c2)

    if c3 <= c2:
        r3 = c1
        r2 = c3
    else:
        c4 = int(np.floor(
            c2 * (1 / aspect_ratio)
        ))
        r3 = c4
        r2 = c2

    r = (r0, r1, r2, r3)
    output_ar = r2 / r3

    assert abs(output_ar - aspect_ratio) <= tolerance, "Output aspect ratio is {} but the specified aspect ratio was {} exceeded by tolerance bounds by more than abs({})".format(output_ar, aspect_ratio, tolerance)

    print("AR corrected crop r:\t {}".format(r))
    print("Desired AR: {} Output AR: {}".format(aspect_ratio, r2 / r3))
    return r
    #print("c1: {} c2: {} c3: {}".format(c1, c2, c3))
    

def crop_single(args, input_path, output_path, output_path_rgb, rgb_bands):
    
    input_path, output_path, output_path_rgb, rgb_bands, r = select_roi(
                                                                        input_path,
                                                                        output_path,
                                                                        output_path_rgb,
                                                                        rgb_bands
    )

    crop_and_save(
        input_path,
        output_path,
        output_path_rgb,
        rgb_bands,
        r
    )

def crop_multi(args, input_path, output_path, output_path_rgb, rgb_bands):
    
    while(True):
        print("Specify output filename (\"cancel\" to exit ROI selection):")
        output_filename = input()
        output_path = 'data/output/' + output_filename + '.hdr'
        if output_filename == 'cancel':
            break
        input_path, output_path, output_path_rgb, rgb_bands, r = select_roi(
                                                                        input_path,
                                                                        output_path,
                                                                        output_path_rgb,
                                                                        rgb_bands
        )

        if args.aspect_ratio:
            r = specific_aspect_ratio(args, r)

        crop_and_save(
            input_path,
            output_path,
            output_path_rgb,
            rgb_bands,
            r
        )


def main(args):
    INPUTPATH = args.filename
    OUTPUTPATH = 'data/output/cropped.hdr'
    OUTPUT_RGB = 'data/output/RGB.png'

    RGBBANDS = [10, 20, 30]

    if args.aspect_ratio:
        print(args.aspect_ratio)

    if args.multi:
        crop_multi(
            args,
            INPUTPATH,
            OUTPUTPATH,
            OUTPUT_RGB,
            RGBBANDS
        )
    else:
        crop_single(
            args,
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

    parser.add_argument(
        '-a',
        '--aspect_ratio',
        type=int,
        help='crop aspect ratio in percent (W x H) x 100'
    )

    args = parser.parse_args()

    output_dir = pathlib.Path('data/output')
    output_dir.mkdir(exist_ok=True, parents=True)

    main(args)