from app.parser import read_data
from app.chunker import chunk_data

data = read_data()
chunked_data = chunk_data(data)

print(f"Total chunks: {len(chunked_data)}")
corrupted_count = sum(1 for entry in chunked_data if entry["is_corrupted"])
print(f"Corrupted chunks: {corrupted_count}")
print()

for entry in chunked_data:
    status = "CORRUPTED" if entry["is_corrupted"] else "ok"
    print(f"[{status}] {entry['source']} chunk {entry['chunk_index']}: {entry['text'][:70]}")