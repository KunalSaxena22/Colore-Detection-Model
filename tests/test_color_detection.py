"""Unit tests for color palette loading and nearest-color matching."""

import tempfile
import unittest
from pathlib import Path

from color_detection import ColorRecord, find_closest_color, get_color_name, load_color_palette


class FindClosestColorTests(unittest.TestCase):
    def setUp(self):
        self.palette = [
            ColorRecord("Black", 0, 0, 0),
            ColorRecord("Red", 255, 0, 0),
            ColorRecord("White", 255, 255, 255),
        ]

    def test_returns_nearest_color(self):
        self.assertEqual(get_color_name(250, 8, 5, self.palette), "Red")

    def test_returns_exact_match(self):
        result = find_closest_color(255, 255, 255, self.palette)
        self.assertEqual(result, ColorRecord("White", 255, 255, 255))

    def test_rejects_empty_palette(self):
        with self.assertRaisesRegex(ValueError, "palette is empty"):
            find_closest_color(1, 2, 3, [])

    def test_rejects_out_of_range_rgb(self):
        with self.assertRaisesRegex(ValueError, "between 0 and 255"):
            find_closest_color(256, 0, 0, self.palette)


class LoadColorPaletteTests(unittest.TestCase):
    def test_loads_six_column_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "colors.csv"
            csv_path.write_text(
                'red,"Bright Red",#ff0000,255,0,0\n'
                'blue,"Deep Blue",#0000ff,0,0,255\n',
                encoding="utf-8",
            )

            palette = load_color_palette(csv_path)

        self.assertEqual(
            palette,
            [
                ColorRecord("Bright Red", 255, 0, 0),
                ColorRecord("Deep Blue", 0, 0, 255),
            ],
        )

    def test_rejects_invalid_csv_row(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "colors.csv"
            csv_path.write_text('red,"Broken",#ff0000,255,0\n', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "expected 6 columns"):
                load_color_palette(csv_path)

    def test_rejects_empty_palette(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "colors.csv"
            csv_path.write_text("", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "No valid colors"):
                load_color_palette(csv_path)


if __name__ == "__main__":
    unittest.main()
