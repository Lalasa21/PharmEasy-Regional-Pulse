### PART-3 : Draft Report, Insight Narrative & Human Review Gate
###STEP - 1: CII insight generator

import metrics_engine

def draft_report_v1(flagged_regions, metrics):

    # If there are no flagged regions
    if len(flagged_regions) == 0:
        return {
            "status": "no_issue",
            "report": []
        }

    # Remove duplicate regions
    unique_regions = list(set(flagged_regions))
    report = []
    for region in unique_regions:
        block = {
            "region": region,
            "Context": "Regional sales movement was flagged for review.",
            "Insight": {},
            "Implication": "The movement should be reviewed before taking action."
        }

        # April -> May
        if region in metrics["april_may_changes"]:
            block["Insight"]["April_to_May"] = round(
                metrics["april_may_changes"][region], 2
            )

        # May -> June
        if region in metrics["may_june_changes"]:
            block["Insight"]["May_to_June"] = round(
                metrics["may_june_changes"][region], 2
            )

        report.append(block)

    return {
        "status": "pending_review",
        "draft_report": report
    }


# Test the function
if __name__ == "__main__":

    # Calculate April -> May
    april_may = metrics_engine.calculate_changes(
        "2026-04",
        "2026-05"
    )

    # Calculate May -> June
    may_june = metrics_engine.calculate_changes(
        "2026-05",
        "2026-06"
    )

    # Find flagged regions
    flagged_april_may = metrics_engine.flag_significant_regions_v1(
        april_may
    )

    flagged_may_june = metrics_engine.flag_significant_regions_v1(
        may_june
    )

    # Combine both lists
    flagged_regions = flagged_april_may + flagged_may_june

    # Keep the results into the metrics dictionary
    metrics = {
        "april_may_changes": april_may,
        "may_june_changes": may_june
    }

    # Create the report
    result = draft_report_v1(
        flagged_regions,
        metrics
    )

    print(result)