import json
import faiss
from sentence_transformers import SentenceTransformer


# Load FAISS vector database
index = faiss.read_index(
    "../datasets/mozilla/bug_vectors.index"
)

# Load historical bug information
with open(
    "../datasets/mozilla/vector_metadata.json",
    "r",
    encoding="utf-8"
) as file:
    metadata = json.load(file)


# Load the same embedding model used by the RAG pipeline
model = SentenceTransformer("all-MiniLM-L6-v2")


# Configurable similarity threshold
DUPLICATE_THRESHOLD = 0.65
RELATED_THRESHOLD = 0.45


def detect_duplicates(
    title,
    description,
    stack_trace="",
    error_logs=""
):
    """
    Duplicate Detection Agent

    Searches historical bugs using semantic similarity
    and classifies the submitted bug as:
    - Duplicate
    - Related
    - New/Unmatched
    """

    # Create searchable text
    bug_text = f"""
Title: {title}

Description: {description}

Stack Trace:
{stack_trace}

Error Logs:
{error_logs}
""".strip()

    # Create embedding for submitted bug
    query_embedding = model.encode(
        [bug_text],
        normalize_embeddings=True
    ).astype("float32")

    # Search top historical matches
    scores, indices = index.search(
        query_embedding,
        3
    )

    matches = []

    for score, index_number in zip(
        scores[0],
        indices[0]
    ):
        historical_bug = metadata[index_number]

        similarity = round(float(score), 4)

        matches.append({
            "bug_id": historical_bug["bug_id"],
            "similarity_score": similarity,
            "summary": historical_bug.get(
                "metadata", {}
            ).get(
                "component",
                "Historical bug"
            ),
            "historical_bug": historical_bug["text"],
            "resolution_summary": (
                "Historical resolution information "
                "is not available in the current "
                "seed dataset."
            ),
            "reason": (
                f"This bug was retrieved because it has "
                f"a semantic similarity score of {similarity} "
                f"with the submitted bug."
            )
        })

    # Determine duplicate status using best match
    if not matches:
        duplicate_status = "New/Unmatched"
        status_reason = (
            "No historical bug matches were found."
        )

    else:
        best_score = matches[0]["similarity_score"]

        if best_score >= DUPLICATE_THRESHOLD:
            duplicate_status = "Duplicate"
            status_reason = (
                f"The best historical match has a "
                f"similarity score of {best_score}, "
                f"which is above the duplicate threshold "
                f"of {DUPLICATE_THRESHOLD}."
            )

        elif best_score >= RELATED_THRESHOLD:
            duplicate_status = "Related"
            status_reason = (
                f"The best historical match has a "
                f"similarity score of {best_score}, "
                f"which indicates a related issue."
            )

        else:
            duplicate_status = "New/Unmatched"
            status_reason = (
                f"The best historical match has a "
                f"similarity score of {best_score}, "
                f"which is below the related-issue threshold."
            )

    return {
        "duplicate_status": duplicate_status,
        "status_reason": status_reason,
        "matching_bugs": matches,
        "thresholds": {
            "duplicate": DUPLICATE_THRESHOLD,
            "related": RELATED_THRESHOLD
        }
    }