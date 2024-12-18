from io import BytesIO
import re
import requests
from PIL import Image

def validate_url(url):
    """Basic URL validation."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def validate_text_input(text, max_length=200):
    """Validate text inputs to prevent XSS and limit length."""
    if not text:
        return False
    if len(text) > max_length:
        return False
    # Allow alphanumeric, spaces, and common punctuation
    return re.match(r'^[a-zA-Z0-9\s.,!?()-]+$', text) is not None

def validate_short_link(short_link, MAX_SHORT_LINK_LENGTH, MIN_SHORT_LINK_LENGTH):
    """Validate short link format."""
    if not short_link:
        return False
    if len(short_link) < MIN_SHORT_LINK_LENGTH or len(short_link) > MAX_SHORT_LINK_LENGTH:
        return False
    # Ensure only alphanumeric characters and hyphens
    return re.match(r'^[a-zA-Z0-9-]+$', short_link) is not None

def validate_image(image_url):
    """
    Validate image requirements:
    * Minimum dimension 200x200 pixels
    * Maximum file size 8 MB
    """
    try:
        # Download image
        response = requests.get(image_url, timeout=5)
        response.raise_for_status()

        # Check file size (8 MB = 8 * 1024 * 1024 bytes)
        file_size = len(response.content)
        if file_size > 8 * 1024 * 1024:
            return False, "Image exceeds 8 MB size limit"

        # Open image and check dimensions
        with Image.open(BytesIO(response.content)) as img:
            width, height = img.size
            if width < 200 or height < 200:
                return False, "Image dimensions must be at least 200x200 pixels"

        return True, "Image is valid"
    except Exception as e:
        return False, str(e)