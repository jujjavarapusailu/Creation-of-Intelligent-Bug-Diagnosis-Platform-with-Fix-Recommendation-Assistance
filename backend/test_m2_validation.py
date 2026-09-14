from triage_agent import analyze_bug
from log_analysis_agent import analyze_log


print("===================================")
print("M2.4 - Accuracy Validation Testing")
print("===================================")


# -------------------------------
# TRIAGE TEST CASES
# -------------------------------

triage_tests = [
    {
        "name": "Critical Login Crash",
        "title": "Application crashes during login",
        "description": "Application crashes when the user enters valid login details."
    },
    {
        "name": "High Payment Failure",
        "title": "Payment API fails",
        "description": "The payment API fails when processing a transaction."
    },
    {
        "name": "Medium Performance Issue",
        "title": "Application is slow",
        "description": "The application has a performance problem and responds slowly."
    },
    {
        "name": "Low UI Issue",
        "title": "Minor UI issue",
        "description": "There is a small display problem in the settings page."
    }
]


print("\n\n--- TRIAGE AGENT TESTS ---")

for test in triage_tests:

    result = analyze_bug(
        test["title"],
        test["description"]
    )

    print("\nTest:", test["name"])
    print("Severity:", result["severity"])
    print("Priority:", result["priority"])
    print("Component:", result["affected_component"])
    print("Confidence:", result["confidence_score"])


# -------------------------------
# LOG ANALYSIS TEST CASES
# -------------------------------

log_tests = [
    {
        "name": "Null Pointer Exception",
        "log": """
java.lang.NullPointerException: Cannot read property
    at LoginService.authenticate(LoginService.java:45)
    at LoginController.login(LoginController.java:20)
    """
    },
    {
        "name": "Array Index Error",
        "log": """
java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 5
    at PaymentService.processPayment(PaymentService.java:78)
    at PaymentController.pay(PaymentController.java:32)
    """
    },
    {
        "name": "Missing Logs",
        "log": ""
    }
]


print("\n\n--- LOG ANALYSIS AGENT TESTS ---")

for test in log_tests:

    result = analyze_log(
        test["log"],
        ""
    )

    print("\nTest:", test["name"])
    print("Exception:", result["exception_type"])
    print("Error Message:", result["error_message"])
    print("Failure Point:", result["failure_point"])
    print("Code Path:", result["code_path"])
    print("Confidence:", result["confidence_score"])


print("\n\n===================================")
print("M2.4 Validation Testing Completed")
print("===================================")