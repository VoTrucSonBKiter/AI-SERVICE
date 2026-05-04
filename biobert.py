from transformers import pipeline
import os
import warnings

# avoid spamming HF symlink warning on Windows
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

_ner = None

def _load_ner():
    try:
        return pipeline("ner", model="dmis-lab/biobert-base-cased-v1.1", aggregation_strategy="simple")
    except Exception as e:
        warnings.warn(f"Failed loading dmis-lab/biobert-base-cased-v1.1: {e}")
        return None

def get_ner():
    global _ner
    if _ner is None:
        _ner = _load_ner()
    return _ner

def extract_entities(text):
    ner = get_ner()
    if ner is None:
        # model failed to load — return empty stable structure so the app stays up
        return {"symptoms": [], "drugs": []}

    results = ner(text)

    symptoms = []
    drugs = []

    for r in results:
        label = r.get("entity_group") or r.get("entity") or ""
        word = r.get("word") or r.get("token") or ""
        if isinstance(word, list):
            word = " ".join(word)
        if "DISEASE" in label:
            symptoms.append(word)
        if "CHEMICAL" in label:
            drugs.append(word)

    return {
        "symptoms": list(set(symptoms)),
        "drugs": list(set(drugs))
    }