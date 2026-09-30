# MINUTES — Premium Cream & Brown Edition

A Streamlit meeting assistant with a warm cream, espresso, and muted-gold interface.

## Run on Windows
Open the VS Code terminal in this folder:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL shown in the terminal, usually http://localhost:8501.

## Features
- Paste meeting notes or upload a `.txt` transcript
- Extract candidate action items, owners, and deadlines
- Editable action register with status and confidence
- Optional meeting title, date, and team fields
- Export results to CSV or Excel
- Cream, brown, and muted-gold styling

## Note
This is a rule-based prototype, not a trained language model. It requires no API key and does not send transcript text to an external service. Review extracted suggestions before relying on them.
