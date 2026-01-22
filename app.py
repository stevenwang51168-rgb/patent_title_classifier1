import os
from io import BytesIO

import pandas as pd
from pandas.api.types import CategoricalDtype
from dotenv import load_dotenv
from flask import Flask, request, render_template, send_file

from openai import OpenAI

load_dotenv()

app = Flask(__name__)

client = OpenAI()

# ---------------------------
# CATEGORY ORDER
# ---------------------------
CATEGORY_ORDER = [
    "Biotechnology",
    "Chemical",
    "Electrical",
    "Mechanical",
    "Software",
]

CATEGORY_TYPE = CategoricalDtype(
    categories=CATEGORY_ORDER,
    ordered=True
)

def classify_patent_title(title: str) -> str:
    title = (title or "").strip()
    if not title:
        return "Unknown"

    prompt = (
        "You are a strict classifier.\n"
        f"Classify the patent title into exactly ONE of: {', '.join(CATEGORY_ORDER)}.\n"
        "Return ONLY the category name.\n\n"
        f"Title: {title}"
    )

    response = client.responses.create(
        model="gpt-5.2",
        input=prompt,
    )

    category = (response.output_text or "").strip()

    if category not in CATEGORY_ORDER:
        return "Unknown"

    return category

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            return "No file uploaded.", 400

        patent_data = pd.read_csv(file)

        # ---- REQUIRED COLUMNS CHECK
        required_cols = {"Title", "Publication Number"}
        if not required_cols.issubset(patent_data.columns):
            return "CSV must include 'Title' and 'Publication Number' columns.", 400

        # ---------------------------
        # CLASSIFY
        # ---------------------------
        patent_data["Category"] = patent_data["Title"].apply(classify_patent_title)

        # ---------------------------
        # NORMALIZE PUBLICATION NUMBER
        # (ensures correct numeric ordering)
        # ---------------------------
        patent_data["Publication Number Sort"] = (
            patent_data["Publication Number"]
            .astype(str)
            .str.extract(r"(\d+)")
            .astype(int)
        )

        # ---------------------------
        # GROUP + SECONDARY SORT
        # ---------------------------
        patent_data["Category"] = (
            patent_data["Category"]
            .astype(str)
            .str.strip()
            .astype(CATEGORY_TYPE)
        )

        patent_data = (
            patent_data
            .sort_values(
                by=["Category", "Publication Number Sort"],
                ascending=[True, True]
            )
            .drop(columns=["Publication Number Sort"])
            .reset_index(drop=True)
        )

        # ---------------------------
        # EXPORT
        # ---------------------------
        output = BytesIO()
        patent_data.to_csv(output, index=False)
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="patent_titles_classified.csv",
            mimetype="text/csv",
        )

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)

