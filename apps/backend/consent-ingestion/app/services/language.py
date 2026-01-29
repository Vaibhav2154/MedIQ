from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# For deterministic results
DetectorFactory.seed = 0

def detect_language(text: str) -> str:
    if not text or not text.strip():
        return "en"
    try:
        lang = detect(text)
        return lang
    except LangDetectException:
        return "en"
