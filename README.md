# Deck Design Tools

A collection of Streamlit web applications for deck construction planning and engineering calculations.

## Applications

### 1. Deck Designer (Main App)
**File:** `deck_designer_overall.py`
- Complete deck design calculator
- Joist and beam layout planning
- Material cost estimation
- Railing and skirting calculations
- Layout diagram generation
- PDF export functionality

### 2. Beam Spacing Calculator
**File:** `beam_spacing_app.py`
- IRC 2021 compliant beam spacing calculations
- Supports Southern Pine and Western Cedar
- Various beam sizes and joist spans

### 3. Joist Calculators
- `joist_IRC_prefilled.py` - Pre-filled IRC joist calculations
- `joist_manual_or__irc.py` - Manual joist calculations
- `joist_file_upload.py` - File upload based joist calculations

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run any application:
```bash
streamlit run deck_designer_overall.py
streamlit run beam_spacing_app.py
```

## Deployment

These applications are ready for deployment on:
- [Streamlit Cloud](https://streamlit.io/cloud)
- Heroku
- Any platform supporting Python web applications

## Data Files

The `data/` directory contains Excel files with reference tables for:
- Beam span calculations
- Joist span tables
- Post height requirements
- Fastener specifications 
