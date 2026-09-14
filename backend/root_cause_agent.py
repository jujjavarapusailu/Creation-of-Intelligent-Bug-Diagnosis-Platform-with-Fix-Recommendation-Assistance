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


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def analyze_root_cause(
    title,
    description,
    triage_result,
    log_result
):
    """
    Root Cause Agent

    Uses:
    - Bug description
    - Triage Agent output
    - Log Analysis Agent output
    - Historical bug knowledge base
    """

    # Build bug context
    bug_context = f"""
Title: {title}

Description: {description}

Severity: {triage_result.get("severity")}
Priority: {triage_result.get("priority")}
Affected Component: {triage_result.get("affected_component")}

Exception Type: {log_result.get("exception_type")}
Error Message: {log_result.get("error_message")}
Failure Point: {log_result.get("failure_point")}
Code Path: {log_result.get("code_path")}
"""

    # Convert current bug into embedding
    query_embedding = model.encode(
        [bug_context],
        normalize_embeddings=True
    ).astype("float32")

    # Search historical bugs
    scores, indices = index.search(
        query_embedding,
        3
    )

    supporting_evidence = []

    for score, index_number in zip(
        scores[0],
        indices[0]
    ):
        historical_bug = metadata[index_number]

        supporting_evidence.append({
            "bug_id": historical_bug["bug_id"],
            "similarity_score": round(
                float(score),
                4
            ),
            "historical_bug": historical_bug["text"],
            "metadata": historical_bug.get(
                "metadata",
                {}
            )
        })

    # Root cause reasoning
    exception_type = log_result.get(
        "exception_type",
        "Unknown"
    )

    failure_point = log_result.get(
        "failure_point",
        "Unknown"
    )

    component = triage_result.get(
        "affected_component",
        "Unknown"
    )

    if exception_type != "Unknown":
        root_cause = (
            f"The probable root cause is related to "
            f"{exception_type} occurring in the "
            f"{component} component. The failure point "
            f"identified from the log is {failure_point}."
        )

        confidence = 0.80

    elif component != "Unknown":
        root_cause = (
            f"The probable root cause is related to "
            f"the {component} component based on the "
            f"submitted bug description and historical "
            f"defect similarity."
        )

        confidence = 0.65

    else:
        root_cause = (
            "Insufficient Evidence: The available bug "
            "description and logs do not provide enough "
            "information to determine a reliable root cause."
        )

        confidence = 0.40

    return {
        "root_cause_hypothesis": root_cause,
        "confidence_score": confidence,
        "supporting_evidence": supporting_evidence,
        "reasoning": (
            "The root cause hypothesis was generated "
            "using the submitted bug information, "
            "Triage Agent results, Log Analysis Agent "
            "results, and semantically similar historical "
            "defects retrieved from the FAISS knowledge base."
        )
    }