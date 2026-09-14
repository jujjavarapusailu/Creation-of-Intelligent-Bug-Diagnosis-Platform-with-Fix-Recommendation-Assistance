from triage_agent import analyze_bug


def test_triage_agent():
    result = analyze_bug(
        title="Minor UI issue",
        description="There is a small display issue in the settings page."
    )

    assert result["severity"] == "Low"
    assert result["priority"] == "P4"
    assert result["affected_component"] == "User Interface"
    assert result["confidence_score"] == 0.6
    assert "severity" in result["reasoning"].lower()


if __name__ == "__main__":
    test_triage_agent()
    print("Triage test passed successfully!")