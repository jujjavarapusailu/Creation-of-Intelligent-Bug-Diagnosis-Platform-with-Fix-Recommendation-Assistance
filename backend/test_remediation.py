from triage_agent import analyze_bug
from log_analysis_agent import analyze_log
from root_cause_agent import analyze_root_cause
from duplicate_detection_agent import detect_duplicates
from remediation_agent import generate_remediation


def test_remediation_agent():
    title = "Application crashes during login"

    description = (
        "The application crashes when the user enters "
        "valid login details."
    )

    stack_trace = """
java.lang.NullPointerException: Cannot read property
    at LoginService.authenticate(LoginService.java:45)
    at LoginController.login(LoginController.java:20)
    at Application.main(Application.java:10)
"""

    triage_result = analyze_bug(
        title,
        description
    )

    log_result = analyze_log(
        stack_trace,
        ""
    )

    root_cause_result = analyze_root_cause(
        title,
        description,
        triage_result,
        log_result
    )

    duplicate_result = detect_duplicates(
        title,
        description,
        stack_trace,
        ""
    )

    remediation_result = generate_remediation(
        title,
        description,
        triage_result,
        log_result,
        root_cause_result,
        duplicate_result
    )

    assert "remediation_status" in remediation_result
    assert "root_cause_used" in remediation_result
    assert "overall_confidence" in remediation_result
    assert "recommendations" in remediation_result
    assert "historical_evidence" in remediation_result
    assert "warning" in remediation_result

    assert len(remediation_result["recommendations"]) > 0
    assert remediation_result["overall_confidence"] == 0.8

    for recommendation in remediation_result["recommendations"]:
        assert "recommendation" in recommendation
        assert "implementation_guidance" in recommendation
        assert "confidence_score" in recommendation
        assert "basis" in recommendation


if __name__ == "__main__":
    test_remediation_agent()
    print("Remediation test passed successfully!")