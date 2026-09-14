from duplicate_detection_agent import detect_duplicates


def test_duplicate_detection_agent():
    title = "Application crashes during login"

    description = (
        "The application crashes when the user enters "
        "valid login details."
    )

    stack_trace = """
java.lang.NullPointerException: Cannot read property
    at LoginService.authenticate(LoginService.java:45)
    at LoginController.login(LoginController.java:20)
"""

    result = detect_duplicates(
        title,
        description,
        stack_trace,
        ""
    )

    assert "duplicate_status" in result
    assert "status_reason" in result
    assert "thresholds" in result
    assert "matching_bugs" in result

    assert result["duplicate_status"] in [
        "Duplicate",
        "Related",
        "New/Unmatched"
    ]

    assert len(result["matching_bugs"]) > 0

    for bug in result["matching_bugs"]:
        assert "bug_id" in bug
        assert "similarity_score" in bug
        assert "summary" in bug
        assert "reason" in bug
        assert "resolution_summary" in bug
        assert "historical_bug" in bug


if __name__ == "__main__":
    test_duplicate_detection_agent()
    print("Duplicate detection test passed successfully!")