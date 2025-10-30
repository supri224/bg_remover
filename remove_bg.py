# remove_bg.py
"""
Small wrapper to remove background from a PIL Image using rembg.
Returns a PIL Image with alpha channel (RGBA).
"""

from rembg import remove
from PIL import Image
import io

def remove_background(pil_image):
    """
    pil_image: PIL.Image instance (RGB or RGBA)
    returns: PIL.Image (RGBA) with background removed
    """
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    input_bytes = buf.getvalue()

    output_bytes = remove(input_bytes)
    out_buf = io.BytesIO(output_bytes)
    result = Image.open(out_buf).convert("RGBA")
    return result
