import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

with open("../datasets/mozilla/bug_chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [chunk["text"] for chunk in chunks]

print("Creating local embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True
).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

faiss.write_index(
    index,
    "../datasets/mozilla/bug_vectors.index"
)

with open(
    "../datasets/mozilla/vector_metadata.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(chunks, file, indent=4)

print("\nLocal embeddings created successfully!")
print("Total embeddings:", len(embeddings))
print("Vector dimension:", dimension)
print("FAISS index saved successfully!")