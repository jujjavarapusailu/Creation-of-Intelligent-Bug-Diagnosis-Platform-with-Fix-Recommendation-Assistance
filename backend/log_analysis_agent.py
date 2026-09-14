import re


def analyze_log(stack_trace: str, error_logs: str):
    log_text = f"{stack_trace}\n{error_logs}".strip()

    if not log_text:
        return {
            "exception_type": "Unknown",
            "error_message": "No logs provided",
            "failure_point": "Unknown",
            "code_path": [],
            "confidence_score": 0.0
        }

    # Find exception/error type
    exception_match = re.search(
        r"([A-Za-z0-9_.]+(?:Exception|Error))",
        log_text
    )

    exception_type = (
        exception_match.group(1)
        if exception_match
        else "Unknown"
    )

    # Find error message
    message_match = re.search(
        r"(?:Exception|Error):\s*(.+)",
        log_text
    )

    error_message = (
        message_match.group(1).strip()
        if message_match
        else "Error message not found"
    )

    # Find file, method and line number
    failure_match = re.search(
        r"at\s+([A-Za-z0-9_.$]+)\(([^:]+):(\d+)\)",
        log_text
    )

    if failure_match:
        method = failure_match.group(1)
        file_name = failure_match.group(2)
        line_number = failure_match.group(3)

        failure_point = {
            "file": file_name,
            "method": method,
            "line": int(line_number)
        }
    else:
        failure_point = {
            "file": "Unknown",
            "method": "Unknown",
            "line": None
        }

    # Extract stack trace code path
    code_path = re.findall(
        r"at\s+([A-Za-z0-9_.$]+)\(([^:]+):(\d+)\)",
        log_text
    )

    formatted_code_path = []

    for method, file_name, line_number in code_path:
        formatted_code_path.append({
            "method": method,
            "file": file_name,
            "line": int(line_number)
        })

    # Confidence score
    confidence = 0.5

    if exception_type != "Unknown":
        confidence += 0.2

    if error_message != "Error message not found":
        confidence += 0.1

    if formatted_code_path:
        confidence += 0.2

    return {
        "exception_type": exception_type,
        "error_message": error_message,
        "failure_point": failure_point,
        "code_path": formatted_code_path,
        "confidence_score": round(confidence, 2)
    }