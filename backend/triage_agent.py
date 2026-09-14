from typing import Dict


def analyze_bug(title: str, description: str) -> Dict:
    text = f"{title} {description}".lower()

    # Severity classification
    if any(word in text for word in [
        "crash", "critical", "data loss", "security breach",
        "system down", "cannot start"
    ]):
        severity = "Critical"
        priority = "P1"
        confidence = 0.90

    elif any(word in text for word in [
        "error", "fails", "failure", "not working", "hang"
    ]):
        severity = "High"
        priority = "P2"
        confidence = 0.80

    elif any(word in text for word in [
        "slow", "delay", "performance", 
    ]):
        severity = "Medium"
        priority = "P3"
        confidence = 0.70

    else:
        severity = "Low"
        priority = "P4"
        confidence = 0.60

    # Component detection
    if any(word in text for word in ["login", "password", "authentication"]):
        component = "Authentication"

    elif any(word in text for word in ["database", "sql", "sqlite"]):
        component = "Database"

    elif any(word in text for word in ["ui", "button", "page", "screen"]):
        component = "User Interface"

    elif any(word in text for word in ["api", "server", "backend"]):
        component = "Backend/API"

    elif any(word in text for word in ["network", "connection", "timeout"]):
        component = "Network"

    else:
        component = "Unknown"

    reasoning = (
        f"Classified as {severity} because the bug description "
        f"contains indicators matching the severity rules. "
        f"The affected component is likely {component}."
    )

    return {
        "severity": severity,
        "priority": priority,
        "affected_component": component,
        "confidence_score": confidence,
        "reasoning": reasoning
    }