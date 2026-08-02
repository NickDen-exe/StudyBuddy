from app.parser import read_data
from app.chunker import is_text_corrupted, is_word_mixed_script, MIN_SAMPLE_SIZE

data = read_data()

for entry in data:
    print("---")
    print(entry["source"], entry.get("page", entry.get("paragraph")))
    print(entry["text"][:80])

    words = entry["text"].split()
    mixed_words = [w for w in words if is_word_mixed_script(w)]
    mixed_ratio = len(mixed_words) / len(words) if words else 0.0

    print("mixed_ratio:", round(mixed_ratio, 2))
    print("is_text_corrupted result:", is_text_corrupted(entry["text"]))