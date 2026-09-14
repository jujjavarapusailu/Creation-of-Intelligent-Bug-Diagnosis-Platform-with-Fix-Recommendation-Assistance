async function analyzeBug() {

    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();
    const stackTrace = document.getElementById("stackTrace").value;
    const errorLogs = document.getElementById("errorLogs").value;

    if (!title || !description) {
        alert("Please enter Bug Title and Bug Description.");
        return;
    }

    const loading = document.getElementById("loading");
    const findings = document.getElementById("findings");

    loading.classList.remove("hidden");
    findings.classList.add("hidden");

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/analyze",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    title: title,
                    description: description,
                    stack_trace: stackTrace,
                    error_logs: errorLogs
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Analysis failed"
            );
        }

        displayFindings(data);

    } catch (error) {

        console.error(error);

        alert(
            "Unable to analyze the bug.\n\n" +
            "Make sure the FastAPI backend is running."
        );

    } finally {

        loading.classList.add("hidden");
    }
}


function displayFindings(data) {

    const triage = data.triage_analysis;
    const log = data.log_analysis;
    const root = data.root_cause_analysis;
    const duplicate = data.duplicate_analysis;
    const remediation = data.remediation_analysis;


    // -----------------------------------------
    // Triage
    // -----------------------------------------

    document.getElementById("severity").textContent =
        triage.severity || "-";

    document.getElementById("priority").textContent =
        triage.priority || "-";

    document.getElementById("component").textContent =
        triage.affected_component || "-";

    document.getElementById("triageConfidence").textContent =
        triage.confidence_score ?? "-";

    document.getElementById("triageReasoning").textContent =
        triage.reasoning || "-";


    // -----------------------------------------
    // Log Analysis
    // -----------------------------------------

    document.getElementById("exceptionType").textContent =
        log.exception_type || "-";

    document.getElementById("errorMessage").textContent =
        log.error_message || "-";

    document.getElementById("failurePoint").textContent =
        formatFailurePoint(log.failure_point);

    document.getElementById("logConfidence").textContent =
        log.confidence_score ?? "-";


    document.getElementById("codePath").textContent =
        formatCodePath(log.code_path);


    // -----------------------------------------
    // Root Cause
    // -----------------------------------------

    document.getElementById("rootCause").textContent =
        root.root_cause_hypothesis || "Insufficient Evidence";

    document.getElementById("rootConfidence").textContent =
        root.confidence_score ?? "-";

    document.getElementById("rootReasoning").textContent =
        root.reasoning || "-";


    const rootEvidence =
        document.getElementById("rootEvidence");

    rootEvidence.innerHTML = "";

    if (
        root.supporting_evidence &&
        root.supporting_evidence.length > 0
    ) {

        root.supporting_evidence.forEach(
            evidence => {

                const div =
                    document.createElement("div");

                div.className = "evidence";

                div.innerHTML = `
                    <strong>Bug ID:</strong>
                    ${evidence.bug_id}
                    <br>

                    <strong>Similarity:</strong>
                    ${evidence.similarity_score}
                    <br><br>

                    <strong>Historical Evidence:</strong>
                    <p>${escapeHtml(
                        evidence.historical_bug || ""
                    )}</p>
                `;

                rootEvidence.appendChild(div);
            }
        );

    } else {

        rootEvidence.textContent =
            "Insufficient Evidence";
    }


    // -----------------------------------------
    // Duplicate Detection
    // -----------------------------------------

    document.getElementById("duplicateStatus").textContent =
        duplicate.duplicate_status || "Unknown";

    document.getElementById("duplicateReason").textContent =
        duplicate.status_reason || "-";


    const duplicateMatches =
        document.getElementById("duplicateMatches");

    duplicateMatches.innerHTML = "";

    if (
        duplicate.matching_bugs &&
        duplicate.matching_bugs.length > 0
    ) {

        duplicate.matching_bugs.forEach(
            bug => {

                const div =
                    document.createElement("div");

                div.className = "match";

                div.innerHTML = `
                    <strong>Bug ID:</strong>
                    ${bug.bug_id}
                    <br>

                    <strong>Similarity Score:</strong>
                    ${bug.similarity_score}
                    <br><br>

                    <strong>Reason:</strong>
                    <p>${escapeHtml(
                        bug.reason || ""
                    )}</p>

                    <strong>Resolution:</strong>
                    <p>${escapeHtml(
                        bug.resolution_summary || ""
                    )}</p>
                `;

                duplicateMatches.appendChild(div);
            }
        );

    } else {

        duplicateMatches.textContent =
            "No matching historical bugs found.";
    }


    // -----------------------------------------
    // Remediation
    // -----------------------------------------

    document.getElementById("remediationStatus").textContent =
        remediation.remediation_status || "-";

    document.getElementById("remediationConfidence").textContent =
        remediation.overall_confidence ?? "-";

    const recommendations =
        document.getElementById("recommendations");

    recommendations.innerHTML = "";

    if (
        remediation.recommendations &&
        remediation.recommendations.length > 0
    ) {

        remediation.recommendations.forEach(
            (item, index) => {

                const div =
                    document.createElement("div");

                div.className = "recommendation";

                div.innerHTML = `
                    <h3>
                        Recommendation ${index + 1}
                    </h3>

                    <p>
                        <strong>Recommendation:</strong>
                        ${escapeHtml(
                            item.recommendation || ""
                        )}
                    </p>

                    <p>
                        <strong>Implementation Guidance:</strong>
                        ${escapeHtml(
                            item.implementation_guidance || ""
                        )}
                    </p>

                    <p>
                        <strong>Confidence:</strong>
                        ${item.confidence_score ?? "-"}
                    </p>

                    <p>
                        <strong>Basis:</strong>
                        ${escapeHtml(
                            item.basis || ""
                        )}
                    </p>
                `;

                recommendations.appendChild(div);
            }
        );

    } else {

        recommendations.textContent =
            "Insufficient Evidence";
    }


    // -----------------------------------------
    // Remediation Evidence
    // -----------------------------------------

    const remediationEvidence =
        document.getElementById(
            "remediationEvidence"
        );

    remediationEvidence.innerHTML = "";

    if (
        remediation.historical_evidence &&
        remediation.historical_evidence.length > 0
    ) {

        remediation.historical_evidence.forEach(
            evidence => {

                const div =
                    document.createElement("div");

                div.className = "evidence";

                div.innerHTML = `
                    <strong>Bug ID:</strong>
                    ${evidence.bug_id}
                    <br>

                    <strong>Similarity Score:</strong>
                    ${evidence.similarity_score}
                    <br><br>

                    <p>${escapeHtml(
                        evidence.evidence || ""
                    )}</p>
                `;

                remediationEvidence.appendChild(div);
            }
        );

    } else {

        remediationEvidence.textContent =
            "No historical evidence available.";
    }


    document.getElementById("remediationWarning").textContent =
        remediation.warning ||
        "Recommendations should be verified through testing.";


    // Show complete findings
    document
        .getElementById("findings")
        .classList.remove("hidden");
}


// -----------------------------------------
// Helper Functions
// -----------------------------------------

function formatFailurePoint(point) {

    if (!point || typeof point !== "object") {
        return point || "Unknown";
    }

    return (
        `${point.file || "Unknown"} : ` +
        `${point.method || "Unknown"} : ` +
        `${point.line ?? "Unknown"}`
    );
}


function formatCodePath(path) {

    if (!path || path.length === 0) {
        return "No code path available";
    }

    return path
        .map(item => {

            return (
                `${item.method || "Unknown"} ` +
                `(${item.file || "Unknown"}:` +
                `${item.line ?? "Unknown"})`
            );

        })
        .join("\n");
}


function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}