import re

CHUNK_SIZE = 500
OVERLAP = 50
MIN_SAMPLE_SIZE = 5             # если слов меньше — не доверяем статистике, считаем текст нормальным
MIXED_SCRIPT_THRESHOLD = 0.3    # доля "смешанных" слов, выше которой текст считаем битым

CYRILLIC_RE = re.compile(r'[а-яА-ЯіІїЇєЄґҐ]')
LATIN_RE = re.compile(r'[a-zA-Z]')


def is_word_mixed_script(word):
    return bool(CYRILLIC_RE.search(word)) and bool(LATIN_RE.search(word))


def is_text_corrupted(text):
    words = text.split()
    if len(words) < MIN_SAMPLE_SIZE:
        return False

    mixed_words = [w for w in words if is_word_mixed_script(w)]
    mixed_ratio = len(mixed_words) / len(words)

    return mixed_ratio > MIXED_SCRIPT_THRESHOLD


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks


def chunk_data(data, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunked_records = []
    for entry in data:
        text_chunks = chunk_text(entry["text"], chunk_size, overlap)
        for chunk_index, chunk in enumerate(text_chunks):
            new_entry = entry.copy()
            new_entry["text"] = chunk
            new_entry["chunk_index"] = chunk_index
            chunked_records.append(new_entry)
    return chunked_records