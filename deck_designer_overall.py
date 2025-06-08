# deck_designer_app_integrated.py

import streamlit as st
from io import BytesIO
def export_to_pdf(summary_lines):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary_lines:
        pdf.cell(200, 10, txt=line, ln=True)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return BytesIO(pdf_bytes)
st.set_page_config(page_title="Deck Designer – Integrated", layout="wide")
import math
import matplotlib.pyplot as plt
from io import BytesIO

# Check for optional imports
try:
    from fpdf import FPDF
except ImportError:
    FPDF = None
    st.warning("📄 PDF export disabled — run `pip install fpdf` to enable it.")

# Pricing data for cost estimation
default_pricing = {
    "decking": 12.5,   # $/sq ft
    "railing": 45.0,   # $/linear ft
    "skirting": 8.0    # $/sq ft
}

# Layout diagram generator
def draw_simple_layout(length, width, beam_count, joist_count):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, length)
    ax.set_ylim(0, width)
    for i in range(beam_count + 1):
        x = i * (length / beam_count)
        ax.plot([x, x], [0, width], 'b--', label="Beam" if i == 0 else "")
    for j in range(joist_count + 1):
        y = j * (width / joist_count)
        ax.plot([0, length], [y, y], 'k-', label="Joist" if j == 0 else "")
    ax.set_title("Deck Layout Diagram")
    ax.set_xlabel("Length (ft)")
    ax.set_ylabel("Width (ft)")
    plt.legend()
    return fig

# PDF export
def export_to_pdf(data_summary):
    if not FPDF:
        return None
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in data_summary:
        pdf.cell(200, 10, txt=line, ln=True)
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

# Streamlit UI
st.title("Deck Designer – Joists, Beams, Railings, Skirting, Cost & Export")

# Step 1: Basic Setup
st.header("1. Project Settings")
live_load = st.selectbox("Live Load (psf)", [40, 50, 60, 70, 80, 90], index=0)
joist_spacing = st.selectbox("Joist Spacing (inches o.c.)", [16, 12], index=0)
wood_species = st.selectbox("Wood Species", ["Southern Pine", "Western Cedar"])
deck_type = st.selectbox("Deck Material Type", ["Composite", "PVC", "Wood"])

# Step 2: Dimensions
st.header("2. Deck Dimensions")
deck_length = st.number_input("Deck Length (ft)", min_value=1.0)
deck_width = st.number_input("Deck Width (ft)", min_value=1.0)
area = deck_length * deck_width
perimeter = 2 * (deck_length + deck_width)
st.success(f"Area: {area:.2f} sq ft | Perimeter: {perimeter:.2f} ft")

# Step 3: Ledger Side
st.header("3. Ledger Side")
ledger_side = st.selectbox("Attached Side (ledger)", ["Top", "Bottom", "Left", "Right"])
is_along_length = ledger_side in ["Left", "Right"]

# Step 4: Joist & Beam Layout
st.header("4. Joist & Beam Layout")
joist_span = deck_length if not is_along_length else deck_width
spacing_ft = joist_spacing / 12
joist_count = math.floor((deck_width if not is_along_length else deck_length) / spacing_ft) + 1

max_joist_span = 13.0 if wood_species == "Southern Pine" else 11.0
beam_count = math.ceil((deck_length if not is_along_length else deck_width) / 8.0)
beam_spacing = (deck_length if not is_along_length else deck_width) / beam_count

st.write(f"📏 Joists span: {joist_span:.2f} ft | Count: {joist_count}")
st.write(f"📐 Beams needed: {beam_count} @ {beam_spacing:.2f} ft apart")

# Step 5: Railings
st.header("5. Railing Options")
include_railing = st.checkbox("Include Railings?", value=True)
railing_length = 0
if include_railing:
    railing_type = st.selectbox("Railing Style", ["Standard Picket", "Glass Panel", "Cable"])
    railing_sides = st.multiselect("Railing Sides", ["Top", "Bottom", "Left", "Right"], default=["Top", "Bottom"])
    for side in railing_sides:
        if side in ["Top", "Bottom"]:
            railing_length += deck_length
        else:
            railing_length += deck_width

# Step 6: Skirting
st.header("6. Skirting")
skirting_type = st.selectbox("Skirting Type", ["None", "Vertical", "Horizontal"])
skirting_area = 0
if skirting_type != "None":
    skirt_sides = ["Top", "Bottom", "Left", "Right"]
    skirt_length = sum([
        deck_length if s in ["Top", "Bottom"] else deck_width
        for s in skirt_sides
        if s not in railing_sides
    ])
    skirt_height = st.number_input("Average Skirt Height (ft)", min_value=0.0, value=2.0)
    skirting_area = skirt_length * skirt_height
    st.write(f"Skirt Area: {skirting_area:.2f} sq ft")

# Step 7: Cost Estimator
st.header("7. Cost Estimation")
costs = {
    "decking": area * default_pricing["decking"],
    "railing": railing_length * default_pricing["railing"],
    "skirting": skirting_area * default_pricing["skirting"]
}
total_cost = sum(costs.values())
st.write(f"Decking Cost: ${costs['decking']:.2f}")
st.write(f"Railing Cost: ${costs['railing']:.2f}")
st.write(f"Skirting Cost: ${costs['skirting']:.2f}")
st.subheader(f"💲 Total Estimated Cost: **${total_cost:,.2f}**")

# Step 8: Diagram
st.header("8. Deck Layout Diagram")
fig = draw_simple_layout(deck_length, deck_width, beam_count, joist_count)
st.pyplot(fig)

# Step 9: Export
st.header("9. Export")
if st.button("Download Summary PDF"):
    summary_lines = [
        f"Deck Dimensions: {deck_length} ft x {deck_width} ft"
        f"Ledger Side: {ledger_side}"
        f"Joist Count: {joist_count}, Spacing: {joist_spacing}\""
        f"Beam Count: {beam_count}, Spacing: {beam_spacing:.2f} ft"
        f"Railing Length: {railing_length} ft"
        f"Skirting Area: {skirting_area:.2f} sq ft"
        f"Total Estimated Cost: ${total_cost:,.2f}"
    ]
    pdf_data = export_to_pdf(summary_lines)
    if pdf_data:
        st.download_button("Click to Download PDF", pdf_data, file_name="deck_summary.pdf")
    else:
        st.error("PDF generation not available. Please install fpdf.")

# --- Additional Features ---

# Auto Board Count (simplified assumption)
st.header("🔩 Board Estimation")
board_width_in = 5.5
board_width_ft = board_width_in / 12
boards_needed = math.ceil(deck_width / board_width_ft) * math.ceil(deck_length / max(12, 8))
st.write(f"Estimated deck boards (assuming 12' or 8' lengths): **{boards_needed}**")

# Proposal Formatting
st.header("📧 Proposal Summary")
proposal_text = f"""
Hello,

Attached is the deck design summary:

- Dimensions: {deck_length} ft x {deck_width} ft
- Ledger Side: {ledger_side}
- Joists: {joist_count} @ {joist_spacing}" spacing
- Beams: {beam_count} total
- Railing: {railing_length} linear ft
- Skirting: {skirting_area:.2f} sq ft
- Estimated Total Cost: ${total_cost:,.2f}

Thank you for considering our services!
"""
st.code(proposal_text)

# Deployment Note
st.markdown("✅ *Ready for deployment on [Streamlit Cloud](https://streamlit.io/cloud). Just upload this file and run it online.*")