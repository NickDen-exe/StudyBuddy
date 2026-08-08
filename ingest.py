from app.parser import read_data
from app.chunker import chunk_data
from app.vectorstore import add_chunks


def main():
    print("Reading documents from ./data...")
    data = read_data()
    print(f"Found {len(data)} pages/paragraphs")

    print("Splitting into chunks...")
    chunks = chunk_data(data)
    print(f"Got {len(chunks)} chunks")

    corrupted = [c for c in chunks if c["is_corrupted"]]
    if corrupted:
        print(f"Warning: {len(corrupted)} chunks flagged as corrupted and will be skipped")

    print("Computing embeddings and writing to ChromaDB (this may take a while)...")
    added = add_chunks(chunks)
    print(f"Done: added {added} chunks to the database")


if __name__ == "__main__":
    main()