import re

def extract_first_sentence(text):
    text = text.strip('"').replace('"', '')
    match = re.match(r'([^\.!?]*[\.!?])', text)

    if match:
        return match.group(1).strip()
    else:
        return None