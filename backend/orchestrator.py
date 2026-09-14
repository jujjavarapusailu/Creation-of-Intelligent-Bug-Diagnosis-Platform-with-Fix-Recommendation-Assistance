from triage_agent import analyze_bug
from log_analysis_agent import analyze_log


def analyze_bug_with_agents(
    title: str,
    description: str,
    stack_trace: str = "",
    error_logs: str = ""
):
    # Run Triage Agent
    triage_result = analyze_bug(
        title,
        description
    )

    # Run Log Analysis Agent
    log_result = analyze_log(
        stack_trace,
        error_logs
    )

    # Combine both agent outputs
    bug_context = {
        "bug": {
            "title": title,
            "description": description
        },
        "triage_analysis": triage_result,
        "log_analysis": log_result
    }

    return bug_context