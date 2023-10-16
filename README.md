# Glottis Segmentation Toolkit

This repository offers a comprehensive toolkit for performing glottis segmentation using various algorithms like K-means, MeanShift, and U-Net. It provides a web interface for easy interaction and visualization. Apart from segmenting, the tool computes metrics like glottis surface and provides insights using videos by extracting frames and plotting surface variations.

## Features

- **Segmentation Algorithms:** Leverage K-means, MeanShift, and U-Net for glottis segmentation.
- **Surface Computation:** Calculate and display the surface area of the segmented glottis in pixels.
- **Video Analysis:** Extract frames from videos, identify the frame with the maximum segmented surface, and visualize its mask and surface.
- **Plotting:** Visualize how the glottis surface varies throughout a video sequence.

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/fouedayedi/GlottisSegmentationToolkit.git
```
3. Navigate to the cloned directory and set up the environment (preferably using a virtual environment):
```bash
cd GlottisSegmentationToolkit
python -m venv venv
source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate
pip install -r requirements.txt
```
3. Run the application:
```bash
cd app
python app.py
```
Navigate to the provided localhost URL in your browser.
## Usage

- Upload your image or video data.
- Choose a segmentation algorithm from K-means, MeanShift, or U-Net.
- For videos, the tool will extract frames and display metrics like the maximum glottis surface. You can also view a plot showing the variation of glottis surface throughout the video.

## Source Code

For the model training source code, please visit the [GitHub Repository](https://github.com/fouedayedi/U-Net-Model-for-Glottis-Segmentation).
