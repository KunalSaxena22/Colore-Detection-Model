# Color Detection Model

A small Python/OpenCV desktop utility that lets you inspect an image and identify the nearest named color from the included RGB palette.

## Features

- Open a local image and double-click a pixel to sample its color.
- Match the sampled RGB value to the closest entry in `colors.csv` using Manhattan RGB distance.
- Display the matched color name and exact sampled RGB values.
- Close the viewer with **Q**, **Esc**, or the window close button.
- Validate image paths, image decoding, palette entries, and RGB channel values before opening the viewer.

## Requirements

- Python 3.10 or newer.
- OpenCV for Python.

Install the dependency:

~~~bash
python -m pip install -r requirements.txt
~~~

## Usage

Run from the repository root and provide an image path:

~~~bash
python color_detection.py path/to/image.jpg
~~~

You can also run the program without an image argument and enter the path when prompted:

~~~bash
python color_detection.py
~~~

The default palette is the `colors.csv` file stored beside `color_detection.py`. To use another compatible six-column palette:

~~~bash
python color_detection.py path/to/image.jpg --colors path/to/colors.csv
~~~

The CSV columns are: color identifier, display name, hex value, red, green, and blue. RGB channel values must be integers from 0 through 255.

## Tests

The color matching and CSV validation helpers have unit tests using Python's standard library:

~~~bash
python -m unittest discover -s tests -v
~~~

These tests do not open an image window.

## Project files

- `color_detection.py`: image viewer, click handling, palette loading, and color matching.
- `colors.csv`: named RGB color palette.
- `requirements.txt`: Python runtime dependency.
- `tests/test_color_detection.py`: unit tests for palette loading and matching.

## License

This repository currently does not include a `LICENSE` file. Contact the maintainer before redistributing or reusing the project.

## Maintainer

Kunal Saxena — [@KunalSaxena22](https://github.com/KunalSaxena22)
