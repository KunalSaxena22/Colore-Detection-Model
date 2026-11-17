"""Interactive color picker for images using a CSV color palette."""

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import cv2


@dataclass(frozen=True)
class ColorRecord:
    """A named RGB color loaded from the palette CSV."""

    name: str
    red: int
    green: int
    blue: int


def _validate_rgb(red: int, green: int, blue: int) -> None:
    """Raise ValueError unless all channels are integers from 0 through 255."""
    channels = (red, green, blue)
    if any(not isinstance(channel, int) or not 0 <= channel <= 255 for channel in channels):
        raise ValueError("RGB channels must be integers between 0 and 255.")


def load_color_palette(csv_path: Path) -> list[ColorRecord]:
    """Load the six-column color dataset and validate every RGB entry."""
    palette: list[ColorRecord] = []

    try:
        with csv_path.open("r", newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.reader(csv_file)
            for line_number, row in enumerate(reader, start=1):
                if not row:
                    continue
                if len(row) < 6:
                    raise ValueError(
                        f"Invalid color entry on line {line_number}: expected 6 columns."
                    )

                name = row[1].strip()
                if not name:
                    raise ValueError(
                        f"Invalid color entry on line {line_number}: color name is empty."
                    )

                try:
                    red, green, blue = (int(value.strip()) for value in row[3:6])
                except ValueError as error:
                    raise ValueError(
                        f"Invalid RGB value on line {line_number}: {error}"
                    ) from error

                _validate_rgb(red, green, blue)
                palette.append(ColorRecord(name, red, green, blue))
    except OSError as error:
        raise OSError(f"Unable to read color palette '{csv_path}': {error}") from error

    if not palette:
        raise ValueError(f"No valid colors were found in '{csv_path}'.")

    return palette


def find_closest_color(
    red: int, green: int, blue: int, palette: Sequence[ColorRecord]
) -> ColorRecord:
    """Return the palette entry with the smallest Manhattan RGB distance."""
    _validate_rgb(red, green, blue)
    if not palette:
        raise ValueError("The color palette is empty.")

    return min(
        palette,
        key=lambda color: (
            abs(red - color.red)
            + abs(green - color.green)
            + abs(blue - color.blue)
        ),
    )


def get_color_name(
    red: int, green: int, blue: int, palette: Sequence[ColorRecord]
) -> str:
    """Return the closest matching color name for an RGB pixel."""
    return find_closest_color(red, green, blue, palette).name


def _on_mouse_click(event, x, y, flags, state) -> None:
    """Record the RGB value and nearest palette color for a double-click."""
    if event != cv2.EVENT_LBUTTONDBLCLK:
        return

    image = state["image"]
    height, width = image.shape[:2]
    if not (0 <= x < width and 0 <= y < height):
        return

    blue, green, red = (int(channel) for channel in image[y, x][:3])
    match = find_closest_color(red, green, blue, state["palette"])
    state["selection"] = {
        "red": red,
        "green": green,
        "blue": blue,
        "name": match.name,
    }


def _draw_selection(frame, selection) -> None:
    """Draw a color swatch and readable label without modifying the source image."""
    if selection is None:
        return

    height, width = frame.shape[:2]
    if height < 2 or width < 2:
        return

    red = selection["red"]
    green = selection["green"]
    blue = selection["blue"]
    swatch_bgr = (blue, green, red)

    bar_height = min(58, height - 1)
    cv2.rectangle(frame, (0, 0), (width - 1, bar_height), swatch_bgr, thickness=-1)

    # Use perceived brightness to keep the label readable on light and dark swatches.
    brightness = (0.299 * red) + (0.587 * green) + (0.114 * blue)
    text_color = (0, 0, 0) if brightness >= 150 else (255, 255, 255)
    label = (
        f"{selection['name']}  "
        f"R={red} G={green} B={blue}"
    )
    font_scale = min(0.65, max(0.35, width / 1100))
    baseline_y = min(bar_height - 8, max(18, int(bar_height * 0.68)))

    cv2.putText(
        frame,
        label,
        (10, baseline_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        text_color,
        thickness=1,
        lineType=cv2.LINE_AA,
    )


def run_color_detector(image_path: Path, colors_path: Path) -> None:
    """Open the image and run the interactive color picker."""
    if not image_path.is_file():
        raise FileNotFoundError(f"Image file not found: '{image_path}'.")

    palette = load_color_palette(colors_path)
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(
            f"OpenCV could not decode '{image_path}'. Check that it is a supported image."
        )

    state = {"image": image, "palette": palette, "selection": None}
    window_name = "Color Detection"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, _on_mouse_click, state)

    try:
        while True:
            frame = image.copy()
            _draw_selection(frame, state["selection"])
            cv2.imshow(window_name, frame)

            # Close with Q or Esc, or by clicking the window's close button.
            if cv2.waitKey(20) & 0xFF in (ord("q"), 27):
                break
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
    finally:
        cv2.destroyAllWindows()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Double-click an image to identify its nearest named RGB color."
    )
    parser.add_argument(
        "image",
        nargs="?",
        help="Path to the image to inspect. If omitted, you will be prompted.",
    )
    parser.add_argument(
        "--colors",
        type=Path,
        default=Path(__file__).resolve().with_name("colors.csv"),
        help="Path to the six-column colors CSV (default: colors.csv beside this script).",
    )
    args = parser.parse_args()

    image_value = args.image or input("Enter the path of the image file: ").strip()
    if not image_value:
        parser.error("An image path is required.")

    try:
        run_color_detector(Path(image_value).expanduser(), args.colors.expanduser())
    except (FileNotFoundError, OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
