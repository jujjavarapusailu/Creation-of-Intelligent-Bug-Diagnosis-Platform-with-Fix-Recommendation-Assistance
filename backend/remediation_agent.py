def generate_remediation(
    title,
    description,
    triage_result,
    log_result,
    root_cause_result,
    duplicate_result
):
    """
    Remediation Agent

    Uses:
    - Triage Agent
    - Log Analysis Agent
    - Root Cause Agent
    - Duplicate Detection Agent

    Generates actionable remediation recommendations.
    """

    recommendations = []

    severity = triage_result.get(
        "severity",
        "Unknown"
    )

    component = triage_result.get(
        "affected_component",
        "Unknown"
    )

    exception_type = log_result.get(
        "exception_type",
        "Unknown"
    )

    failure_point = log_result.get(
        "failure_point",
        "Unknown"
    )

    root_cause = root_cause_result.get(
        "root_cause_hypothesis",
        "Unknown"
    )

    root_confidence = root_cause_result.get(
        "confidence_score",
        0.0
    )

    duplicate_status = duplicate_result.get(
        "duplicate_status",
        "New/Unmatched"
    )

    # ------------------------------------------------
    # Recommendation based on exception information
    # ------------------------------------------------

    if exception_type != "Unknown":

        recommendations.append({
            "recommendation": (
                f"Investigate and fix the {exception_type} "
                f"at the identified failure point: "
                f"{failure_point}."
            ),
            "implementation_guidance": (
                "Review the variables and objects used at "
                "the failure point. Add appropriate null "
                "checks, input validation, or exception "
                "handling where required."
            ),
            "confidence_score": 0.80,
            "basis": "Agent reasoning based on log analysis"
        })

    # ------------------------------------------------
    # Recommendation based on affected component
    # ------------------------------------------------

    if component != "Unknown":

        recommendations.append({
            "recommendation": (
                f"Review the {component} component for "
                "the code path associated with the reported "
                "failure."
            ),
            "implementation_guidance": (
                "Check recent changes in the affected module, "
                "validate input handling, and add regression "
                "tests covering the failing scenario."
            ),
            "confidence_score": 0.70,
            "basis": "Agent reasoning based on triage analysis"
        })

    # ------------------------------------------------
    # Recommendation based on duplicate detection
    # ------------------------------------------------

    if duplicate_status in [
        "Duplicate",
        "Related"
    ]:

        recommendations.append({
            "recommendation": (
                "Review the matching historical defects "
                "and reuse applicable resolution approaches "
                "before implementing a new fix."
            ),
            "implementation_guidance": (
                "Compare the current failure with the "
                "historical bug's component, error pattern, "
                "and resolution. Adapt the previous solution "
                "only after verifying that the same root cause "
                "is present."
            ),
            "confidence_score": 0.75,
            "basis": "Historical similarity evidence"
        })

    # ------------------------------------------------
    # General best-practice recommendation
    # ------------------------------------------------

    recommendations.append({
        "recommendation": (
            "Add a regression test for the reported failure "
            "scenario after applying the fix."
        ),
        "implementation_guidance": (
            "Reproduce the bug, apply the fix, run the new "
            "regression test, and verify that existing tests "
            "continue to pass."
        ),
        "confidence_score": 0.65,
        "basis": "General software engineering best practice"
    })

    # ------------------------------------------------
    # Determine overall confidence
    # ------------------------------------------------

    if root_confidence >= 0.80:
        overall_confidence = 0.80

    elif root_confidence >= 0.60:
        overall_confidence = 0.65

    else:
        overall_confidence = 0.45

    # ------------------------------------------------
    # Evidence
    # ------------------------------------------------

    supporting_evidence = root_cause_result.get(
        "supporting_evidence",
        []
    )

    historical_evidence = []

    for evidence in supporting_evidence:

        historical_evidence.append({
            "bug_id": evidence.get("bug_id"),
            "similarity_score": evidence.get(
                "similarity_score"
            ),
            "evidence": evidence.get(
                "historical_bug"
            )
        })

    # ------------------------------------------------
    # Final result
    # ------------------------------------------------

    return {
        "bug_title": title,

        "remediation_status": (
            "Recommendations Generated"
        ),

        "root_cause_used": root_cause,

        "overall_confidence": overall_confidence,

        "recommendations": recommendations,

        "historical_evidence": historical_evidence,

        "warning": (
            "These recommendations are suggestions, "
            "not confirmed fixes. The implementation "
            "should be verified through testing and "
            "code review."
        )
    }