import os
import pandas as pd
import streamlit as st
from openai import OpenAI
from pandas.api.types import CategoricalDtype

client = OpenAI()

CATEGORY_ORDER = ["Chemical", "Biotechnology", "Electrical", "Mechanical", "Software"]
CATEGORY_TYPE = CategoricalDtype(categories=CATEGORY_ORDER, ordered=True)

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
    resp = client.responses.create(model="gpt-5.2", input=prompt)
    cat = (resp.output_text or "").strip()
    return cat if cat in CATEGORY_ORDER else "Unknown"

st.title("Patent Title Classification App")

uploaded = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)

    if "Title" not in df.columns or "Publication Number" not in df.columns:
        st.error("CSV must include 'Title' and 'Publication Number' columns.")
        st.stop()

    with st.spinner("Classifying titles..."):
        df["Category"] = df["Title"].apply(classify_patent_title)

    # publication number numeric sort key
    df["Publication Number Sort"] = (
        df["Publication Number"].astype(str).str.extract(r"(\d+)").astype(int)
    )

    # group + secondary sort
    df["Category"] = df["Category"].astype(str).str.strip().astype(CATEGORY_TYPE)
    df = (
        df.sort_values(["Category", "Publication Number Sort"])
          .drop(columns=["Publication Number Sort"])
          .reset_index(drop=True)
    )

    st.success("Done!")
    st.dataframe(df)

    out = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download classified CSV",
        data=out,
        file_name="patent_titles_classified.csv",
        mime="text/csv",
    )
