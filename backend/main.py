


from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from orchestrator import analyze_bug_with_agents
from root_cause_agent import analyze_root_cause
from duplicate_detection_agent import detect_duplicates
from remediation_agent import generate_remediation


app = FastAPI(title="AI Bug Analysis System")


bugs = []


class BugReport(BaseModel):
    title: str
    description: str
    stack_trace: str = ""
    error_logs: str = ""


@app.get("/")
def home():
    return {
        "message": "AI Bug Analysis System API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/bugs")
def submit_bug(bug: BugReport):

    if not bug.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Bug title is required"
        )

    if not bug.description.strip():
        raise HTTPException(
            status_code=400,
            detail="Bug description is required"
        )

    bug_data = bug.model_dump()

    bugs.append(bug_data)

    return {
        "message": "Bug submitted successfully",
        "bug": bug_data
    }


@app.get("/bugs")
def get_bugs():

    return {
        "total_bugs": len(bugs),
        "bugs": bugs
    }


@app.post("/bugs/upload")
async def upload_bug_file(
    file: UploadFile = File(...)
):

    content = await file.read()

    try:

        text_content = content.decode("utf-8")

    except UnicodeDecodeError:

        return {
            "message": (
                "Unable to read file. "
                "Please upload a text file."
            )
        }

    return {
        "message": "Bug file uploaded successfully",
        "filename": file.filename,
        "size": len(content),
        "content": text_content
    }


# ------------------------------------------------
# COMPLETE AI BUG ANALYSIS
# ------------------------------------------------

@app.post("/analyze")
def analyze_bug(bug: BugReport):

    if not bug.title.strip():

        raise HTTPException(
            status_code=400,
            detail="Bug title is required"
        )

    if not bug.description.strip():

        raise HTTPException(
            status_code=400,
            detail="Bug description is required"
        )

    try:

        # -----------------------------------------
        # M2.3
        # Triage + Log Analysis
        # -----------------------------------------

        initial_analysis = analyze_bug_with_agents(
            title=bug.title,
            description=bug.description,
            stack_trace=bug.stack_trace,
            error_logs=bug.error_logs
        )

        triage_result = initial_analysis[
            "triage_analysis"
        ]

        log_result = initial_analysis[
            "log_analysis"
        ]


        # -----------------------------------------
        # M3.1
        # Root Cause Agent
        # -----------------------------------------

        root_cause_result = analyze_root_cause(
            title=bug.title,
            description=bug.description,
            triage_result=triage_result,
            log_result=log_result
        )


        # -----------------------------------------
        # M3.2
        # Duplicate Detection Agent
        # -----------------------------------------

        duplicate_result = detect_duplicates(
            title=bug.title,
            description=bug.description,
            stack_trace=bug.stack_trace,
            error_logs=bug.error_logs
        )


        # -----------------------------------------
        # M3.3
        # Remediation Agent
        # -----------------------------------------

        remediation_result = generate_remediation(
            title=bug.title,
            description=bug.description,
            triage_result=triage_result,
            log_result=log_result,
            root_cause_result=root_cause_result,
            duplicate_result=duplicate_result
        )


        # -----------------------------------------
        # Complete structured result
        # -----------------------------------------

        return {

            "bug": {
                "title": bug.title,
                "description": bug.description,
                "stack_trace": bug.stack_trace,
                "error_logs": bug.error_logs
            },

            "triage_analysis": triage_result,

            "log_analysis": log_result,

            "root_cause_analysis": root_cause_result,

            "duplicate_analysis": duplicate_result,

            "remediation_analysis": remediation_result

        }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Bug analysis failed: {str(error)}"
        )