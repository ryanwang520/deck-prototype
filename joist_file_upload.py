
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Joist Span Checker", layout="wide")

st.title("📏 Joist Span Validation Tool")

# Upload the joist span spreadsheet
uploaded_file = st.file_uploader("Upload your Joist Span Table (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        joist_df = pd.read_excel(uploaded_file)

        st.success("✅ Spreadsheet loaded successfully!")
        st.dataframe(joist_df.head())

        joist_size = st.selectbox("Select Joist Size", joist_df['Joist Size'].unique())
        spacing = st.selectbox("Select Joist Spacing (inches o.c.)", sorted(joist_df['Spacing'].unique()))
        deck_span = st.number_input("Enter Deck Total Span (ft)", min_value=1.0, step=0.5)

        filtered = joist_df[
            (joist_df['Joist Size'] == joist_size) &
            (joist_df['Spacing'] == spacing)
        ]

        if not filtered.empty:
            max_span = filtered['Max Span (ft)'].values[0]
            if deck_span <= max_span:
                st.success(f"✅ Approved. Max span for {joist_size} at {spacing} o.c. is **{max_span} ft**.")
            else:
                st.error(f"❌ Not Approved. Max span for {joist_size} at {spacing} o.c. is only **{max_span} ft**, but you entered **{deck_span} ft**.")
        else:
            st.warning("⚠️ No matching data found for selected joist size and spacing.")

    except Exception as e:
        st.error(f"❌ Error loading file: {e}")