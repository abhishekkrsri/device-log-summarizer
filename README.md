# Device Log Summarizer CLI

A Python command-line project for summarizing device telemetry from a CSV file.

## Files
- `main.py`: CSV ingestion, grouping, statistics, filtering, JSON export, terminal table.
- `chart.py`: loads `summary.json` and creates `average_temperature.png`.
- `tests_section1.py`: test expectations for Section 1; complete the function in `main.py` yourself.
- `device_telemetry.csv`: illustrative sample input. Replace it with the assessment-provided file.
- `summary.json`: illustrative sample output; regenerate it after completing Section 1 and running the project.
- `PROMPT_LOG.md`: document the actual AI prompting/debugging process.

## Setup (Windows / VS Code)
1. Install Python 3 if needed.
2. Open this folder in VS Code.
3. In the VS Code terminal, optionally create a virtual environment:
   `python -m venv .venv`
4. Activate it in PowerShell:
   `.\.venv\Scripts\Activate.ps1`
5. Install chart dependency:
   `python -m pip install matplotlib`

## Run
After completing `clean_sensor_readings()` in `main.py` yourself:
- `python main.py`
- `python chart.py`
- `python tests_section1.py`

## Notes
- The included CSV is illustrative because the actual assessment CSV was not supplied with this chat. Replace it with the file supplied by the assessor.
- Section 1 has an intentional TODO to respect the assessment's no-AI requirement.
- The aggregation counts rows with a valid `device_id` as total records, counts `ERROR` statuses independently of temperature validity, and excludes invalid/non-finite temperatures from averages.
- Devices with no valid temperatures are excluded because their average is undefined.
- Filtering removes devices only when their average is strictly greater than 80.0.
