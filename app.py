import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from src.simulation import run_simulation_round
from src.database import init_db, save_result, load_results, DB_PATH

st.set_page_config(page_title="AI Red vs Blue Cybersecurity Simulation", layout="wide")

init_db()

st.title("AI Red vs Blue Cybersecurity Simulation")


# ---------------- SIDEBAR ----------------
st.sidebar.header("Simulation Controls")

num_rounds = st.sidebar.number_input(
    "Number of rounds to run",
    min_value=1,
    max_value=50,
    value=1,
    step=1
)

if st.sidebar.button("Run Simulation"):
    for _ in range(num_rounds):
        result = run_simulation_round()
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

if rows:
    columns = [
        "id", "timestamp", "attack_type", "difficulty", "message",
        "true_label", "predicted_label", "confidence", "explanation"
    ]
    df = pd.DataFrame(rows, columns=columns)

    # Filter
    filter_label = st.sidebar.selectbox(
        "Filter by true label",
        ["All", "malicious", "benign"]
    )

    if filter_label != "All":
        df = df[df["true_label"] == filter_label]

    latest = df.iloc[0]


    # ---------------- MAIN DISPLAY ----------------
    st.subheader("Latest Attack")
    st.write(latest["message"])

    st.subheader("Blue Team Result")
    st.write(f"**Predicted Label:** {latest['predicted_label']}")
    st.write(f"**Confidence:** {latest['confidence']}")
    st.write(f"**Explanation:** {latest['explanation']}")

    st.subheader("Simulation History")
    st.dataframe(df, width="stretch")


    # ---------------- METRICS ----------------
    total = len(df)
    correct = (df["true_label"] == df["predicted_label"]).sum()
    accuracy = correct / total if total > 0 else 0

    true_positive = ((df["true_label"] == "malicious") & (df["predicted_label"] == "malicious")).sum()
    true_negative = ((df["true_label"] == "benign") & (df["predicted_label"] == "benign")).sum()
    false_positive = ((df["true_label"] == "benign") & (df["predicted_label"] == "malicious")).sum()
    false_negative = ((df["true_label"] == "malicious") & (df["predicted_label"] == "benign")).sum()

    precision = precision_score(df["true_label"], df["predicted_label"], pos_label="malicious")
    recall = recall_score(df["true_label"], df["predicted_label"], pos_label="malicious")
    f1 = f1_score(df["true_label"], df["predicted_label"], pos_label="malicious")

    st.subheader("Metrics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rounds", total)
    col2.metric("Correct Detections", correct)
    col3.metric("Accuracy", f"{accuracy:.2%}")

    col4, col5, col6, col7 = st.columns(4)
    col4.metric("True Positives", true_positive)
    col5.metric("True Negatives", true_negative)
    col6.metric("False Positives", false_positive)
    col7.metric("False Negatives", false_negative)

    col8, col9, col10 = st.columns(3)
    col8.metric("Precision", f"{precision:.2f}")
    col9.metric("Recall", f"{recall:.2f}")
    col10.metric("F1 Score", f"{f1:.2f}")



    # ---------------- Recent Errors ----------------

    errors_df = df[df["true_label"] != df["predicted_label"]]

    st.subheader("Recent Misclassifications")
    if not errors_df.empty:
        st.dataframe(errors_df, width="stretch")
    else:
        st.success("No misclassifications found in the current dataset.")

    

    # ---------------- CHARTS ----------------
    st.subheader("Charts")

    label_counts = df["true_label"].value_counts()
    st.write("**True Label Distribution**")
    st.bar_chart(label_counts)

    prediction_counts = df["predicted_label"].value_counts()
    st.write("**Predicted Label Distribution**")
    st.bar_chart(prediction_counts)

    attack_type_counts = df["attack_type"].value_counts()
    st.write("**Attack Type Distribution**")
    st.bar_chart(attack_type_counts)

    st.write("**Confusion Matrix**")
    cm = confusion_matrix(
        df["true_label"],
        df["predicted_label"],
        labels=["benign", "malicious"]
    )

    fig, ax = plt.subplots()
    ax.imshow(cm)

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["benign", "malicious"])
    ax.set_yticklabels(["benign", "malicious"])
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    ax.set_title("Confusion Matrix")

    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center")

    st.pyplot(fig)


    # ---------------- EXPORT ----------------
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="simulation_results.csv",
        mime="text/csv"
    )

else:
    st.info("No simulation rounds have been run yet.")