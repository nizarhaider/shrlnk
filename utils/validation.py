import re


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
