
import streamlit as st

st.set_page_config(page_title="Joist Span Entry – Manual or IRC", layout="centered")
st.title("🧮 Joist Span Entry")

mode = st.radio("Choose entry mode:", ["Manual Entry", "Prefill from IRC 2021 Table"])

if mode == "Manual Entry":
    st.subheader("Manual Joist Span Inputs")
    wood_species = st.multiselect("Wood Species", ["Southern Pine", "Western Cedar"])
    joist_size = st.multiselect("Joist Size", ["2x6", "2x8", "2x10", "2x12"])
    joist_spacing = st.multiselect("Joist Spacing (inches on center)", [12, 16, 24])
    live_load = st.multiselect("Live Load (psf)", [40, 50, 60, 70])
    max_cantilever = st.multiselect("Max Cantilever Joist Back Span (ft)", [4, 6, 8, 10, 12, 14, 16, 18])

    if st.button("Submit Manual Entry"):
        if wood_species and joist_size and joist_spacing and live_load and max_cantilever:
            for species in wood_species:
                for size in joist_size:
                    for spacing in joist_spacing:
                        for live in live_load:
                            for cant in max_cantilever:
                                st.success(
                                    f"✅ Entry recorded: {species} {size}, {spacing} o.c., Live Load: {live} psf, Cantilever: {cant} ft."
                                )
        else:
            st.error("❌ Please select at least one option for each field.")
else:
    st.subheader("Prefill from 2021 IRC Table")
    st.info("📚 This would prefill values using predefined IRC 2021 joist span data. Coming soon...")
