# hyperspectral-image-cropper

## 🧐 About <a name = "about"></a>
A simple Python tool based on [OpenCV](https://opencv.org/) and [Spectral Python (SPy)](http://www.spectralpython.net/) for cropping datacubes of hyperspectral images.

## 🏁 Getting Started <a name = "getting_started"></a>

#### Create your hyperspectral dataset
In `roi.py`, specify the file you from where you want to extract your ROIs from. Then

```bash
python3 roi.py
```

to crop your data.

#### Training
```bash
python3 train.py
```
This will load the images in the dataset path, and preprocess them into a feasible Keras dataset type.
Then it will train the model. It should take a few seconds on a decent GPU.

This function will also run `test.py` after training.

#### Test
```bash
python3 test.py
```

Run test dataset.

#### Inference
```
python3 inference.py
```

This will run prediction on the whole hyperspectral image, and classify each pixel as pharmaceutical or background.

> Note: The function for plotting the legend is not very good, so the printed labels may be wrong. However the classifications are correct anyway.

#### Dataset
The dataset is provided by Professor Lise Lyngsnes Randeberg at the Department of Electronic Systems, Norwegian University of Science and Technology (NTNU).

## ⛏️ Dependencies
* python 3.8.3
* numpy 1.18.1
* matplotlib 3.1.3
* keras

## ✍️ Author
- Bendik Austnes [@kidneb7](https://github.com/kidneb7)


## :camera: Data provider
- [Professor Lise Lyngsnes Randeberg](https://www.ntnu.edu/employees/lise.randeberg)