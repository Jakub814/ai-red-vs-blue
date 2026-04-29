# AI Red vs Blue Cybersecurity Simulation

## Overview

AI Red vs Blue is a safe cybersecurity simulation platform developed as a Final Year Project prototype. It models the interaction between a Red Team and a Blue Team in a controlled environment, where the Red Team generates synthetic phishing-style messages and the Blue Team analyses them using implemented defence modes including rule-based, ML-based, and hybrid detection.

The project is designed to explore how AI-driven attacks and AI-assisted defences can be simulated, measured, and visualised without deploying real malware, sending real phishing emails, or interacting with external targets. The emphasis is on safety, explainability, repeatability, and academic evaluation.

## Aim
The aim of the project is to build a working software prototype that demonstrates how a Red Team vs Blue Team simulation can be implemented using Python, machine learning, local persistence, and a simple dashboard interface.


## Current Features
- Dynamic Red Team generation of benign and malicious text samples
- Multiple Blue Team defence modes: rule-based, ML-based, and hybrid
- Explanation output alongside each Blue Team prediction
- SQLite database for local result storage
- Streamlit dashboard for running and reviewing simulations
- Multiple simulation rounds in a single run
- Accuracy, precision, recall, F1 score, and attack success rate
- Confusion matrix visualisation
- Recent misclassification review
- Misclassifications by difficulty analysis
- Confidence filtering and filtered result review
- CSV export of simulation results


## Project Scope
This project is a simulation prototype only. It does **not**:
- send phishing emails
- deploy malware
- interact with real accounts or external systems
- perform offensive actions outside the local test environment

All attack content is synthetic and generated purely for safe academic experimentation.

## Tech Stack
- **Python** – core programming language
- **Streamlit** – dashboard and user interface
- **SQLite** – local database storage
- **pandas** – data handling and metrics processing
- **scikit-learn** – machine-learning classifier
- **matplotlib** – confusion matrix visualisation
- **joblib** – model saving/loading

## Project Structure
```text
ai-red-vs-blue/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── check_db.py
├── db/
│   └── (created at runtime)
├── models/
│   └── phishing_detector.joblib
└── src/
    ├── blue_team.py
    ├── database.py
    ├── red_team.py
    ├── simulation.py
    └── train_model.py
```
## File Descriptions
### app.py

Main Streamlit application.
Provides the dashboard interface for:
- running simulation rounds
- selecting defence mode
- selecting generation difficulty
- viewing the latest attack and detection result
- displaying stored simulation history
- showing metrics, charts, and confusion matrix
- reviewing misclassifications
- exporting results to CSV

### src/red_team.py

Implements the Red Team generator.
Produces synthetic benign and malicious messages with randomized wording, brands, names, and difficulty levels.

### src/blue_team.py

Coordinates a single simulation round.
It calls the Red Team generator, sends the message to the selected Blue Team defence mode, and returns the completed result object.

### src/simulation.py

Coordinates a single simulation round.
Calls the Red Team generator, sends the message to the Blue Team defence mode, and returns the completed result object.

### src/database.py

Handles SQLite database setup and data storage.
Responsible for:
- creating the database
- inserting simulation results
- loading stored results

### src/train_model.py

Trains and saves the phishing detection model using predefined benign and malicious training examples.

### check_db.py

Simple helper script used to inspect stored SQLite data directly in the terminal.

## How the System Works
1. The Red Team generates a synthetic text sample.
2. The sample is labelled internally as either benign or malicious.
3. The Simulation Engine sends the sample to the selected Blue Team defence mode.
4. The Blue Team classifier predicts the label and returns:
    - predicted label
    - confidence
    - explanation
5. The result is stored in SQLite.
6. The dashboard displays:
    - latest message
    - prediction
    - metrics
    - charts
    - misclassifications
    - historical results
      
## How to Run the Project
### 1. Create and activate a virtual environment

On Windows PowerShell:
```text
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies
```text
pip install -r requirements.txt
```
If needed, install the main packages manually:
```text
pip install streamlit pandas matplotlib scikit-learn joblib
```

### 3. Train the model
```text
python src/train_model.py
```
This creates:
```text
models/phishing_detector.joblib
```
### 4. Run the Streamlit app
```text
python -m streamlit run app.py
```

Alternative:
```text
streamlit run app.py
```
### 5. Open the app

Once running, Streamlit should provide a local URL such as:
```text
http://localhost:8501
```
Open that in your browser.

##  Dashboard Functionality
### Simulation Controls

The sidebar allows the user to:
- choose how many rounds to run
- choose generation difficulty
- choose Blue Team defence mode
- filter results by true label
- filter results by minimum confidence
- start a simulation batch
- reset the database

### Main Output
The dashboard displays:
- latest generated attack/message
- Blue Team classification result
- true label
- attack type
- difficulty
- defence mode
- confidence score
- explanation text

### Metrics
The dashboard calculates:
- total rounds
- correct detections
- accuracy
- true positives
- true negatives
- false positives
- false negatives
- precision
- recall
- F1 score
- attack success rate

### Charts
The dashboard includes:
- true label distribution
- predicted label distribution
- attack type distribution
- difficulty distribution
- confidence by predicted label
- misclassifications by difficulty
- confusion matrix

### Misclassification Review
The dashboard includes a recent misclassifications section to help analyse missed malicious cases and other classification errors.

### Export
Users can download results as a CSV file.

## Example Use Cases
- Demonstrate a safe AI Red vs Blue simulation for an academic audience
- Compare rule-based, ML-based, and hybrid defensive approaches
- Show how phishing-style text can be classified by a lightweight ML pipeline
- Run repeated rounds to generate evaluation data
- Compare benign and malicious outcomes over time
- Produce screenshots and results for dissertation chapters

## Safety and Ethics
This project is intentionally constrained for safe academic use:
- all messages are synthetic
- execution is local
- no real phishing delivery occurs
- no malware is generated
- no external systems are targeted
The project is designed to align with the ethical and legal constraints discussed in the dissertation.

## Current Limitations
- The generated dataset is still synthetic and relatively small
- The classifier is lightweight and intended for prototype-scale experimentation
- The current evaluation environment is local only
- The dashboard is functional rather than enterprise-grade
- Final results remain dependent on controlled synthetic generation rather than live operational data
These limitations are acceptable for the scope of a Final Year Project and are discussed in the dissertation as part of the prototype evaluation.

## Possible Future Improvements
- Larger and more varied synthetic datasets
- More advanced phishing generation logic
- Stronger classifier training and validation
- More formal comparative testing across defence modes
- Enhanced explanation techniques
- More advanced dashboard filtering and analytics
- User testing and usability feedback
- Deployment in a contained lab/test environment

## Author
**Jakub Leszczynski**<br>
Bachelor of Science (Honours) in Software Development<br>
Final Year Project

## License
This project is for academic and educational use only.
