import json
import faiss
from sentence_transformers import SentenceTransformer

index = faiss.read_index("../datasets/mozilla/bug_vectors.index")

with open("../datasets/mozilla/vector_metadata.json", "r", encoding="utf-8") as file:
    metadata = json.load(file)

model = SentenceTransformer("all-MiniLM-L6-v2")

query = input("Enter your bug description: ")

query_embedding = model.encode(
    [query],
    normalize_embeddings=True
).astype("float32")

scores, indices = index.search(query_embedding, 3)

print("\nSimilar historical bugs:\n")

for score, index_number in zip(scores[0], indices[0]):
    bug = metadata[index_number]

    print("Bug ID:", bug["bug_id"])
    print("Similarity Score:", round(float(score), 4))
    print("Details:")
    print(bug["text"])
    print("-" * 60)