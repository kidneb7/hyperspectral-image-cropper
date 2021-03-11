# hyperspectral-image-cropper

## 🧐 About <a name = "about"></a>
A simple Python tool based on [OpenCV](https://opencv.org/) and [Spectral Python (SPy)](http://www.spectralpython.net/) for cropping datacubes of hyperspectral images.

## 🏁 Getting Started <a name = "getting_started"></a>

#### Setting up the environment
Using Anaconda, run

```bash
conda env create -f environment.yml
```

from the repository root folder.

#### Crop hyperspectral cubes
From the repository root folder, run

```bash
python3 roi.py -f path_to_hyperspectral_file.hdr -m
```

to crop multiple regions of interest from `path_to_hyperspectral_file.hdr`. Before each crop, specify the name of the cropped file without file extension. Then in the OpenCV window, select ROI and confirm with `SPACE` or `ENTER`. Both a hyperspectral cube (`.hdr`) and an RGB preview (`.png`) will be saved to the `data/outputs/`  directory.

> Omitting `-m` disables multiple crops and the output will be saved as `cropped.hdr`.


## ⛏️ Dependencies
* python
* numpy
* matplotlib
* OpenCV
* Spectral Python (SPy)

## ✍️ Author
- Bendik Austnes [@kidneb7](https://github.com/kidneb7)


## :camera: Example data provider
- [Professor Lise Lyngsnes Randeberg](https://www.ntnu.edu/employees/lise.randeberg)