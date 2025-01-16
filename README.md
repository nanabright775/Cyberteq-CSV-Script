# Cyberteq-CSV-Script
To work on the vulnerability csv in cyberteq
Installation
Create The virtual env: `pip -m venv venv`
Activate the virtual environment:

Windows: `venv\Scripts\activate`

macOS/Linux: `source venv/bin/activate`

install the requirements: `pip install -r requirements.txt`

commands to run: `python script_name.py \
    --vulnerability "/path/to/vulnerability5.csv" \
    --jira "/path/to/Jira5.csv" \
    --intermediate_output "/path/to/updated_vulnerability5.csv" \
    --final_output "/path/to/final_processed_vulnerability.csv" \
    --vulnerabilities "vulnerability_title_1,vulnerability_title_2,vulnerability_title_3"`
