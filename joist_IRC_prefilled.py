import streamlit as st

st.set_page_config(page_title="Joist Entry Tool", layout="wide")

st.title("Joist Span Entry – Manual or IRC 2021 Prefilled")

mode = st.radio("Select Mode", ["Manual Entry", "Prefill from IRC 2021 Table"])

if mode == "Manual Entry":
    st.subheader("Manual Entry Form")

    wood_species = st.multiselect("Wood Species", ["Southern Pine", "Western Cedar"])
    joist_sizes = st.multiselect("Joist Sizes", ["2x6", "2x8", "2x10", "2x12"])
    joist_spacings = st.multiselect("Joist Spacing (inches)", [12, 16, 24])
    live_loads = st.multiselect("Live Load (psf)", [40, 50, 60, 70])
    cantilevers = st.multiselect("Max Cantilever Back Span (ft)", [4, 6, 8, 10, 12, 14, 16, 18])

    if st.button("Submit Entries"):
        if all([wood_species, joist_sizes, joist_spacings, live_loads, cantilevers]):
            st.success("✅ Entries recorded:")
            for species in wood_species:
                for size in joist_sizes:
                    for spacing in joist_spacings:
                        for load in live_loads:
                            for cant in cantilevers:
                                st.write(
                                    f"• {species} {size}, {spacing}\" o.c., {load} psf, Max Cantilever: {cant} ft"
                                )
        else:
            st.warning("Please select values for all fields.")

else:
    st.subheader("Prefilled IRC 2021 Span Lookup")

    # Sample IRC span values
    irc_spans = {
        ("Southern Pine", "2x8", 12): 13.6,
        ("Southern Pine", "2x8", 16): 12.3,
        ("Southern Pine", "2x10", 12): 17.5,
        ("Southern Pine", "2x10", 16): 15.8,
        ("Western Cedar", "2x8", 12): 12.6,
        ("Western Cedar", "2x8", 16): 11.0,
        ("Western Cedar", "2x10", 12): 16.1,
        ("Western Cedar", "2x10", 16): 14.4,
    }

    st.markdown("### Query a specific IRC span")
    species = st.selectbox("Wood Species", ["Southern Pine", "Western Cedar"])
    size = st.selectbox("Joist Size", ["2x8", "2x10"])
    spacing = st.selectbox("Joist Spacing (inches)", [12, 16])
    live = 40

    key = (species, size, spacing)
    if key in irc_spans:
        span = irc_spans[key]
        st.success(f"✅ Max allowable span for {species} {size} @ {spacing}\" o.c. (40 psf): **{span} ft**")
    else:
        st.error("❌ No data found for that combination.")

    st.markdown("---")
    st.markdown("### 📘 IRC 2021 Standard Joist Spans – 40 psf Live Load")

    for s in ["Southern Pine", "Western Cedar"]:
        st.markdown(f"**{s}**")
        for sz in ["2x8", "2x10"]:
            for sp in [12, 16]:
                k = (s, sz, sp)
                if k in irc_spans:
                    st.write(f"• {sz} @ {sp}\" o.c.: {irc_spans[k]} ft")
