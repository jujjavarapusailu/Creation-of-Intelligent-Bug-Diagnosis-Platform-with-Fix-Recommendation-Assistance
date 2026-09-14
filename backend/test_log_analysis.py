from log_analysis_agent import analyze_log


def test_log_analysis_without_logs():
    result = analyze_log("", "")

    assert result["exception_type"] == "Unknown"
    assert result["error_message"] == "No logs provided"
    assert result["failure_point"] == "Unknown"
    assert result["code_path"] == []
    assert result["confidence_score"] == 0.0


if __name__ == "__main__":
    test_log_analysis_without_logs()
    print("Log analysis test passed successfully!")