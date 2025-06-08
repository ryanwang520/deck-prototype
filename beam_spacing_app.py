
import streamlit as st
import pandas as pd

# Page config must come first
st.set_page_config(page_title="Beam Spacing Calculator", layout="wide")

# Hardcoded simplified IRC beam span data
beam_data = [
    {"Species": "Southern Pine", "Beam Size": "2 – 2 × 8", "Joist Span (ft)": 6, "Max Beam Spacing (ft)": 8},
    {"Species": "Southern Pine", "Beam Size": "2 – 2 × 10", "Joist Span (ft)": 8, "Max Beam Spacing (ft)": 6},
    {"Species": "Southern Pine", "Beam Size": "3 – 2 × 10", "Joist Span (ft)": 10, "Max Beam Spacing (ft)": 5.5},
    {"Species": "Western Cedar", "Beam Size": "2 – 2 × 8", "Joist Span (ft)": 6, "Max Beam Spacing (ft)": 7.5},
    {"Species": "Western Cedar", "Beam Size": "2 – 2 × 10", "Joist Span (ft)": 8, "Max Beam Spacing (ft)": 6},
    {"Species": "Western Cedar", "Beam Size": "3 – 2 × 10", "Joist Span (ft)": 10, "Max Beam Spacing (ft)": 5},
]

beam_df = pd.DataFrame(beam_data)

st.title("📏 Beam Spacing Calculator (IRC 2021)")

st.markdown("This tool uses hardcoded span data for **Southern Pine** and **Western Cedar**.")

species = st.selectbox("Select Wood Species", sorted(beam_df["Species"].unique()))
beam_size = st.selectbox("Select Beam Size", sorted(beam_df["Beam Size"].unique()))
joist_span = st.number_input("Enter Joist Span (ft)", min_value=1.0, step=0.5)

filtered_df = beam_df[(beam_df["Species"] == species) & (beam_df["Beam Size"] == beam_size)]
matches = filtered_df[filtered_df["Joist Span (ft)"] >= joist_span]

if not matches.empty:
    result = matches.iloc[0]
    st.success(f"✅ Max Beam Spacing for {species}, {beam_size} with {joist_span} ft joist span: **{result['Max Beam Spacing (ft)']} ft**")
else:
    st.error("❌ No matching data found for the given inputs.")

st.divider()
st.subheader("📚 Prefilled Examples")

examples = [
    ("Southern Pine", "2 – 2 × 8", 6),
    ("Southern Pine", "2 – 2 × 10", 8),
    ("Southern Pine", "3 – 2 × 10", 10),
    ("Western Cedar", "2 – 2 × 8", 6),
    ("Western Cedar", "2 – 2 × 10", 8),
    ("Western Cedar", "3 – 2 × 10", 10),
]

for sp, size, span in examples:
    row = beam_df[(beam_df["Species"] == sp) & (beam_df["Beam Size"] == size) & (beam_df["Joist Span (ft)"] == span)]
    if not row.empty:
        spacing = row.iloc[0]["Max Beam Spacing (ft)"]
        with st.expander(f"{sp}, {size}, Joist Span: {span} ft"):
            st.write(f"➡️ Max Beam Spacing: **{spacing} ft**")
    else:
        st.warning(f"No example found for {sp}, {size}, Span {span} ft")
