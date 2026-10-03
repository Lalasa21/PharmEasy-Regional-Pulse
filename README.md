## Setup

Install Python 3.10 or newer before continuing. `requirements.txt` installs Python packages, not the Python interpreter itself. Download Python from [python.org](https://www.python.org/downloads/); on Windows, enable Add python.exe to PATH in the installer.

Verify the installation in PowerShell:

**python --version**

Then, from the repository root, create and activate a virtual environment and install the project dependencies.

**python -m venv .venv**
**.\.venv\Scripts\Activate.ps1**
If Powershell blocks activation: **Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass**
**python -m pip install --upgrade pip**
**python -m pip install -r requirements.txt**

Run the commands below from the repository root.

## Run Order

The raw data and region lookup CSVs are included in the repository. To reproduce the processed data and dashboard:

1. Copy the script provided and create new file as 'generate_dataset.py'.Then,generate the deterministic input CSVs. This overwrites `pharmeasy_orders_raw.csv` and `regions_master.csv`.

	**python generate_dataset.py**

2. Clean the raw orders and create `orders_clean.csv`.

	**python clean_data.py**

3. Validate the cleaned data schema.

	**python validate_schema.py**

4. Create or refresh `pharmeasy.db` from the cleaned orders and region lookup.

	**python build_db.py**

5. Run the SQL join, duplicate, regional count, and monthly sales checks.

	**python queries.py**

6. Calculate monthly changes and flagged regions, then generate the draft CII report.

	**python metrics_engine.py**
	**python draft_report.py**
	
7. Run **python review_gate.py** to exercise the approve/edit/reject review flow. It appends test entries to `audit_log.jsonl`.

8. Launch the live dashboard. Streamlit prints a local URL in the terminal(http://localhost:****/)

	**python streamlit run app.py**

======================================================================================

### Headline Finding

Guntur's sales increased by 122.19% from April to May, making it a significant regional movement for review.

### Four Evaluation Artifacts

- Streamlit dashboard (`app.py`): live data exploration.
- CII narrative (embedded in `app.py`): explains what the data means.
- One-page memo (`memo.md`): the recommendation based on the movement.
- Presentation storyline (`presentation_storyline.md`): how to defend the finding live.

### Recommended Reviewer Consumption Order

1. Dashboard 
2. Embedded CII Narrative 
3. One-Page Memo
4. Presentation Storyline

This order moves from data exploration, to interpretation, to recommendation, and finally to how the analysis would be defended live.

### Unverified Assumption

No external cause, such as competitor activity or festival demand, is assumed because it is not established by this dataset.[LOW]