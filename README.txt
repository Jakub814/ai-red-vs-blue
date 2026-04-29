AI RED VS BLUE CYBERSECURITY SIMULATION
Jakub Leszczynski

This project is also available on GitHub for easier viewing:
https://github.com/Jakub814/ai-red-vs-blue/tree/main

PROJECT OVERVIEW
This project is a safe cybersecurity simulation platform developed as part of a Final Year Project in Software Development.
It simulates Red Team vs Blue Team interactions in a controlled local environment.

The Red Team generates synthetic phishing-style messages.
The Blue Team detects and classifies those messages using implemented defence modes:
- rule-based
- ml-based
- hybrid

The application stores simulation results locally, calculates evaluation metrics, and displays results in a Streamlit dashboard.

IMPORTANT SAFETY NOTE
This project is a simulation only.
It does not send phishing emails, deploy malware, or interact with live external systems.
All attack content is synthetic and intended only for safe academic experimentation.

==================================================
FILES INCLUDED
==================================================

Main files:
- app.py
- README.TXT
- requirements.txt

Folders:
- src/
- models/
- screenshots/

Important source files:
- src/red_team.py
- src/blue_team.py
- src/simulation.py
- src/database.py
- src/train_model.py

==================================================
SOFTWARE REQUIRED
==================================================

Before running the project, install:
- Python 3.x
- pip

Recommended:
- Python 3.11 or later

==================================================
HOW TO SET UP THE ENVIRONMENT
==================================================

1. Extract the zip file to a folder on your computer.

2. Open a terminal / PowerShell inside the project folder.

3. Create a virtual environment:
python -m venv venv

4. Activate the virtual environment on Windows PowerShell:
venv\Scripts\activate

5. Install the required packages:
pip install -r requirements.txt

If requirements.txt does not work correctly, install the main packages manually:
pip install streamlit pandas matplotlib scikit-learn joblib

==================================================
HOW TO RUN THE PROJECT
==================================================

1. Make sure the virtual environment is activated.

2. Train the model first:
python src/train_model.py

This will create the trained model file used by the application.

3. Run the Streamlit application:
python -m streamlit run app.py

If this works, Streamlit will display a local URL such as:
http://localhost:8501

Open that URL in your browser.

==================================================
HOW TO USE THE APPLICATION
==================================================

1. Open the dashboard in the browser.
2. Select the number of rounds to run.
3. Select the generation difficulty:
- All
- easy
- medium
- hard

4. Select the Blue Team defence mode:
- rule_based
- ml_based
- hybrid

5. Click "Run Simulation".
6. Review the results shown in the dashboard.

The dashboard displays:
- latest attack
- prediction result
- confidence
- explanation
- simulation history
- metrics
- attack success rate
- misclassifications
- charts
- confusion matrix

==================================================
EXPORTING RESULTS
==================================================

The dashboard includes a button to export results as CSV.

==================================================
TROUBLESHOOTING
==================================================

If "streamlit" is not recognised:
Use:
python -m streamlit run app.py

If the application says a package is missing:
Install it with pip, for example:
pip install matplotlib

If the model file is missing:
Run:
python src/train_model.py

If the database causes issues during testing:
Delete the local database file and rerun the app so it is recreated.

==================================================
NOTES
==================================================

- The application is designed for local execution.
- The project uses synthetic data only.
- Screenshots of test runs are included in the screenshots folder.
- The project source code has been submitted as a zipped folder as required.

END OF README