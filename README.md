# Network Intrusion Detection App

## Overview
Real-time network traffic analysis with AI/ML integration for intrusion detection.

## Setup
1. Clone the repo
2. Create virtual env: `python -m venv venv`
3. Activate: `venv\\Scripts\\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Usage

### Backend
```
cd backend
python app.py
```

### Frontend
Open `frontend/index.html` in browser.

## Notes
- Ensure `tshark` is installed and in PATH.
- Pre-trained model can be re-trained in `notebooks/train_model.ipynb`.
- Logs printed to console.
