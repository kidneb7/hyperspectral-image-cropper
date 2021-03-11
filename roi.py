import spectral
import spectral.io.envi as envi
import cv2

import numpy as np 
import matplotlib.pyplot as plt

import os 
import itertools # Hmm do I need it

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
        img_subset
    )
    print("Successfully cropped hyperspectral datacube to", output_path, "cropped at", r)



def main():
    INPUTPATH = 'data/pille1_SWIR_320me_SN3517_6000_us_2019-01-21T162350_corr.hdr'
    OUTPUTPATH = 'data/test.hdr'
    OUTPUT_RGB = 'data/rgb.png'

    RGBBANDS = [10, 20, 30]

    select_roi(
        INPUTPATH,
        OUTPUTPATH,
        OUTPUT_RGB,
        RGBBANDS
    )
    pass

if __name__ == "__main__":
    main()