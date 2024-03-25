# Color Detection Model

This Python project uses the OpenCV library to detect and identify colors in an image. It allows the user to double-click on any part of the image, and the program will display the name of the color along with its RGB values.

## Features

- Load an image from the file system
- Double-click on any part of the image to get the color name and RGB values
- Display the color name, RGB values, and a rectangle filled with the detected color
- Exit the program by pressing the 'a' key

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- Pandas (`pandas`)

## Usage

1. Clone the repository or download the source code.
2. Install the required dependencies by running `pip install opencv-python pandas`.
3. Place the `colors.csv` file in the same directory as the `color_detection.py` file.
4. Run the `color_detection.py` script.
5. Enter the path to the image file when prompted.
6. Double-click on any part of the image to get the color name and RGB values.
7. Press 'a' to exit the program.

## File Structure

- `color_detection.py`: The main Python script that runs the color detection program.
- `colors.csv`: A CSV file containing color names and their corresponding RGB values.
- `README.md`: This file, providing instructions and information about the project.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
