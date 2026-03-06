---
name: coloring-page
description: Turn an uploaded photo into a printable black-and-white coloring page.
metadata:
  clawdbot:
    requires:
      bins:
        - python3
---

# coloring-page

Create a printable black-and-white outline coloring page from a photo using OpenCV edge detection.

This skill is designed to be used conversationally:
- You upload an image
- You say: "create a coloring page"
- The assistant runs this skill and sends back the generated PNG

Under the hood, this uses Python + OpenCV with Canny edge detection and adaptive thresholding for lightweight local processing.

## Requirements

- `python3` available in PATH
- Python packages (auto-installed if missing): `opencv-python`, `numpy`

## How the assistant should use this

When a user message includes:
- an attached image (jpg/png/webp)
- and the user asks for a "coloring page"

**Steps:**
1. Check if required Python packages are installed, if not, install them:
   ```bash
   python3 -m pip install opencv-python numpy --user --quiet
   ```
2. Create the conversion script if it doesn't exist (save as `scripts/convert.py`)
3. Run the conversion:
   ```bash
   python3 scripts/convert.py <path-to-uploaded-image> <output.png>
   ```
4. Send the output image back to the user

## Conversion Script

Save this as `scripts/convert.py` in the skill directory:

```python
#!/usr/bin/env python3
import sys
import cv2
import numpy as np

def create_coloring_page(input_path, output_path):
    # Read image
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Cannot read image from {input_path}")
        sys.exit(1)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply bilateral filter to reduce noise while keeping edges sharp
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Detect edges using Canny
    edges = cv2.Canny(filtered, 50, 150)
    
    # Invert edges (black lines on white background)
    inverted = cv2.bitwise_not(edges)
    
    # Save output
    cv2.imwrite(output_path, inverted)
    print(f"Coloring page saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 convert.py <input_image> <output_image>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    create_coloring_page(input_file, output_file)
```

## CLI Examples

### Basic usage

```bash
python3 scripts/convert.py photo.jpg coloring.png
```

### With auto-install

```bash
python3 -m pip install opencv-python numpy --user --quiet && \
python3 scripts/convert.py photo.jpg coloring.png
```

## Notes

- Input must be a raster image (`.jpg`, `.png`, `.webp`, `.bmp`).
- Output is a PNG with black outlines on white background.
- Processing is done locally, no external API calls.
- First run may take a few seconds to install dependencies (~50MB for opencv-python).
- Subsequent runs are fast (<1 second for typical photos).
