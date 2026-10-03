### PART-3 : Draft Report, Insight Narrative & Human Review Gate
### STEP - 4: Review-gate tool with audit log


import json
from datetime import datetime
import uuid

def review_gate_v1(report, decision, reviewer_note=""):

    # Allowed decisions
    allowed_decisions = ["approve", "edit", "reject"]

    # Check decision
    if decision not in allowed_decisions:
        raise ValueError("Decision must be approve, edit, or reject.")

    # Only approved reports can be used downstream
    if decision == "approve":
        downstream_allowed = True
    else:
        downstream_allowed = False

    # Get region
    region = report.get("region", "Unknown")

    # Create run ID
    run_id = str(uuid.uuid4())

    # Create result
    result = {
        "region": region,
        "decision": decision,
        "downstream_allowed": downstream_allowed,
        "reviewer_note": reviewer_note,
        "run_id": run_id
    }

    # Create audit record
    audit_record = {
        "timestamp": datetime.now().isoformat(),
        "run_id": run_id,
        "region": region,
        "decision": decision,
        "reviewer_note": reviewer_note
    }

    # Add record to audit log
    with open("audit_log.jsonl", "a") as file:
        file.write(json.dumps(audit_record) + "\n")

    return result

# Testing

if __name__ == "__main__":

    report = {
        "region": "Guntur",
        "status": "pending_review"
    }

    # APPROVE
    print("\n--- APPROVE ---")
    print("Before:", report)

    result = review_gate_v1(
        report,
        "approve",
        "Numbers checked and approved."
    )

    print("After:", result)

    # EDIT
    print("\n--- EDIT ---")
    print("Before:", report)

    result = review_gate_v1(
        report,
        "edit",
        "Please add more evidence."
    )

    print("After:", result)

    # REJECT
    print("\n--- REJECT ---")
    print("Before:", report)

    result = review_gate_v1(
        report,
        "reject",
        "Evidence needs further checking."
    )

    print("After:", result)

    # INVALID DECISION TEST
    print("\n--- INVALID DECISION ---")

    try:
        review_gate_v1(
            report,
            "wrong"
        )
    except ValueError as error:
        print("Correctly rejected:", error)