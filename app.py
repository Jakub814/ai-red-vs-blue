import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

from src.simulation import run_simulation_round
from src.database import init_db, save_result, load_results, DB_PATH

st.set_page_config(
    page_title="AI Red vs Blue Cybersecurity Simulation",
    layout="wide"
)

init_db()

st.title("AI Red vs Blue Cybersecurity Simulation")
st.caption(
    "A safe Red Team vs Blue Team prototype for generating synthetic phishing-style "
    "messages and evaluating ML-based detection in a controlled environment."
)

# ---------------- SIDEBAR ----------------
st.sidebar.header("Simulation Controls")

num_rounds = st.sidebar.number_input(
    "Number of rounds to run",
    min_value=1,
    max_value=100,
    value=10,
    step=1
)

difficulty_option = st.sidebar.selectbox(
    "Generation difficulty",
    ["All", "easy", "medium", "hard"]
)

label_filter = st.sidebar.selectbox(
    "Filter by true label",
    ["All", "benign", "malicious"]
)

defense_mode = st.sidebar.selectbox(
    "Blue Team defence mode",
    ["ml_based", "rule_based", "hybrid"]
)

min_confidence = st.sidebar.slider(
    "Minimum confidence",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.01
)

selected_difficulty = None if difficulty_option == "All" else difficulty_option

if st.sidebar.button("Run Simulation"):
    for _ in range(num_rounds):
        result = run_simulation_round(selected_difficulty, defense_mode)
        save_result(result)
    st.sidebar.success(f"{num_rounds} simulation round(s) completed and saved.")

if st.sidebar.button("Reset Database"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM simulation_results")
    conn.commit()
    conn.close()
    st.sidebar.warning("Database cleared. Refresh the page if needed.")

# ---------------- LOAD DATA ----------------
rows = load_results()

if not rows:
    st.info("No simulation rounds have been run yet.")
    st.stop()

columns = [
    "id",
    "timestamp",
    "attack_type",
    "difficulty",
    "message",
    "true_label",
    "predicted_label",
    "confidence",
    "explanation",
    "defense_mode"
]

df = pd.DataFrame(rows, columns=columns)



# ---------------- GLOBAL METRICS DATA ----------------
total_all = len(df)
correct_all = (df["true_label"] == df["predicted_label"]).sum()
accuracy_all = correct_all / total_all if total_all > 0 else 0

true_positive_all = ((df["true_label"] == "malicious") & (df["predicted_label"] == "malicious")).sum()
true_negative_all = ((df["true_label"] == "benign") & (df["predicted_label"] == "benign")).sum()
false_positive_all = ((df["true_label"] == "benign") & (df["predicted_label"] == "malicious")).sum()
false_negative_all = ((df["true_label"] == "malicious") & (df["predicted_label"] == "benign")).sum()

malicious_total = (df["true_label"] == "malicious").sum()
attack_success_rate = false_negative_all / malicious_total if malicious_total > 0 else 0

precision_all = precision_score(df["true_label"], df["predicted_label"], pos_label="malicious", zero_division=0)
recall_all = recall_score(df["true_label"], df["predicted_label"], pos_label="malicious", zero_division=0)
f1_all = f1_score(df["true_label"], df["predicted_label"], pos_label="malicious", zero_division=0)



# ---------------- FILTER DISPLAY DATA ----------------
filtered_df = df.copy()

if label_filter != "All":
    filtered_df = filtered_df[filtered_df["true_label"] == label_filter]

filtered_df = filtered_df[filtered_df["confidence"] >= min_confidence]

st.info(
    f"Current experiment: {defense_mode} defence | "
    f"Generation difficulty: {difficulty_option} | "
    f"Rounds requested: {num_rounds} | "
    f"Stored rounds: {total_all} | "
    f"Label filter: {label_filter} | "
    f"Minimum confidence: {min_confidence:.2f}"
)



# ---------------- LATEST RESULT ----------------
latest = df.iloc[0]

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Latest Attack")
    st.write(latest["message"])

    st.subheader("Blue Team Result")
    st.write(f"**Predicted Label:** {latest['predicted_label']}")
    st.write(f"**True Label:** {latest['true_label']}")
    st.write(f"**Attack Type:** {latest['attack_type']}")
    st.write(f"**Difficulty:** {latest['difficulty']}")
    st.write(f"**Defence Mode:** {latest['defense_mode']}")
    st.write(f"**Confidence:** {latest['confidence']:.2f}")
    st.write(f"**Explanation:** {latest['explanation']}")

with col_right:
    st.subheader("Current Dataset Summary")
    st.metric("Stored Rounds", total_all)
    st.metric("Accuracy", f"{accuracy_all:.2%}")
    st.metric("Precision", f"{precision_all:.2f}")
    st.metric("Recall", f"{recall_all:.2f}")
    st.metric("F1 Score", f"{f1_all:.2f}")
    st.metric("Attack Success Rate", f"{attack_success_rate:.2%}")



# ---------------- HISTORY ----------------
st.subheader("Simulation History")

if filtered_df.empty:
    st.warning("No rows match the current filters.")
else:
    st.dataframe(filtered_df, width="stretch")



# ---------------- METRICS ----------------

unique_true_labels = df["true_label"].nunique()
if unique_true_labels < 2:
    st.warning(
        "The current dataset contains only one true-label class. "
        "Run a mixed batch with difficulty set to 'All' for a fuller evaluation."
    )

st.subheader("Evaluation Metrics")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Rounds", total_all)
m2.metric("Correct Detections", correct_all)
m3.metric("Accuracy", f"{accuracy_all:.2%}")
m4.metric("Misclassifications", false_positive_all + false_negative_all)

m5, m6, m7, m8 = st.columns(4)
m5.metric("True Positives", true_positive_all)
m6.metric("True Negatives", true_negative_all)
m7.metric("False Positives", false_positive_all)
m8.metric("False Negatives", false_negative_all)

m9, m10, m11, m12 = st.columns(4)
m9.metric("Precision", f"{precision_all:.2f}")
m10.metric("Recall", f"{recall_all:.2f}")
m11.metric("F1 Score", f"{f1_all:.2f}")
m12.metric("Attack Success Rate", f"{attack_success_rate:.2%}")



# ---------------- MISCLASSIFICATIONS ----------------
st.subheader("Recent Misclassifications")
errors_df = df[df["true_label"] != df["predicted_label"]]

if errors_df.empty:
    st.success("No misclassifications found in the current dataset.")
else:
    st.dataframe(errors_df, width="stretch")

st.write("**Misclassifications Samples by Difficulty**")

if errors_df.empty:
    st.info("No misclassifications available to chart.")
else:
    misclassification_chart = (
        errors_df["difficulty"]
        .value_counts()
        .reindex(["easy", "medium", "hard"], fill_value=0)
    )
    st.bar_chart(misclassification_chart)



# ---------------- CHARTS ----------------
st.subheader("Charts")

c1, c2 = st.columns(2)

with c1:
    st.write("**True Label Distribution**")
    st.bar_chart(filtered_df["true_label"].value_counts())

    st.write("**Attack Type Distribution**")
    st.bar_chart(filtered_df["attack_type"].value_counts())

with c2:
    st.write("**Predicted Label Distribution**")
    st.bar_chart(filtered_df["predicted_label"].value_counts())

    st.write("**Difficulty Distribution**")
    st.bar_chart(filtered_df["difficulty"].value_counts())

# Confidence by label
st.write("**Confidence by Predicted Label**")
confidence_chart = (
    filtered_df.groupby("predicted_label")["confidence"]
    .mean()
    .sort_values(ascending=False)
)
st.bar_chart(confidence_chart)

# ---------------- CONFUSION MATRIX ----------------
st.subheader("Confusion Matrix")

if filtered_df.empty:
    st.warning("No data available for this filter selection.")
else:
    cm = confusion_matrix(
        filtered_df["true_label"],
        filtered_df["predicted_label"],
        labels=["benign", "malicious"]
    )

    tn, fp, fn, tp = cm.ravel()

    fig, ax = plt.subplots(figsize=(5, 5))
    im = ax.imshow(cm)

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["benign", "malicious"])
    ax.set_yticklabels(["benign", "malicious"])
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    ax.set_title("Confusion Matrix")

    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=14)

    st.pyplot(fig)
    plt.close(fig)

# ---------------- EXPORT ----------------
st.subheader("Export Results")

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Results as CSV",
    data=csv,
    file_name="simulation_results.csv",
    mime="text/csv"
)