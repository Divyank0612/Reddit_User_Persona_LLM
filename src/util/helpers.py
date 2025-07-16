import re

def extract_username_from_url(url):
    """
    Extracts the Reddit username from a given Reddit user profile URL.
    
    Args:
        url (str): Reddit user profile URL.
        
    Returns:
        str: Username if extracted successfully, else None.
    """
    pattern = r"https?://(www\.)?reddit\.com/user/([A-Za-z0-9_-]+)/?"
    match = re.match(pattern, url)
    if match:
        return match.group(2)
    else:
        return None
