try:
    from langdetect import detect
except ImportError:
    print("Please install the langdetect library by running 'pip install langdetect'")

def detect_language(text: str) -> str:
    """Detect language from transcribed text."""
    try:
        return detect(text)
    except:
        return "unknown"
