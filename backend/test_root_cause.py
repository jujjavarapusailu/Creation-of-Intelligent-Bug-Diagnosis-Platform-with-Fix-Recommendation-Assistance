from triage_agent import analyze_bug
from log_analysis_agent import analyze_log
from root_cause_agent import analyze_root_cause


def test_root_cause_agent():
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

    assert "root_cause_hypothesis" in root_cause_result
    assert "confidence_score" in root_cause_result
    assert "supporting_evidence" in root_cause_result
    assert "reasoning" in root_cause_result

    assert root_cause_result["confidence_score"] == 0.8
    assert len(root_cause_result["supporting_evidence"]) > 0

    assert "NullPointerException" in root_cause_result["root_cause_hypothesis"]


if __name__ == "__main__":
    test_root_cause_agent()
    print("Root cause test passed successfully!")