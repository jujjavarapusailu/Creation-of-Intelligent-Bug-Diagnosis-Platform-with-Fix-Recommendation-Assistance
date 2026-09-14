from orchestrator import analyze_bug_with_agents


def test_multi_agent_orchestration():
    result = analyze_bug_with_agents(
        title="Application crashes during login",
        description="The application crashes when the user enters valid login details.",
        stack_trace="""
java.lang.NullPointerException: Cannot read property
    at LoginService.authenticate(LoginService.java:45)
    at LoginController.login(LoginController.java:20)
    at Application.main(Application.java:10)
"""
    )

    assert "bug" in result
    assert "triage_analysis" in result
    assert "log_analysis" in result

    assert result["triage_analysis"]["severity"] == "Critical"
    assert result["triage_analysis"]["priority"] == "P1"

    assert result["log_analysis"]["exception_type"] == "java.lang.NullPointerException"
    assert result["log_analysis"]["failure_point"]["file"] == "LoginService.java"
    assert result["log_analysis"]["failure_point"]["line"] == 45


if __name__ == "__main__":
    test_multi_agent_orchestration()
    print("Orchestrator test passed successfully!")