# Network Intrusion Detection System (NIDS)

## Overview
This project is a real-time Network Intrusion Detection System (NIDS) built with Python, Flask, and machine learning. It captures live network traffic, extracts features, and uses an IsolationForest anomaly detection model to identify potential intrusions. The system provides a web interface for monitoring and analyzing network activity.

## Features
- **Real-time Packet Capture:** Uses TShark (Wireshark CLI) to capture live network packets and save them as `.pcap` files.
- **Feature Extraction:** Extracts relevant features from captured packets for analysis.
- **Machine Learning Detection:** Utilizes an IsolationForest model for anomaly detection, trained on real network data.
- **Web Interface:** Flask backend serves results and provides endpoints for starting captures and viewing analysis.
- **Extensible Design:** Modular codebase for easy extension and experimentation.

## Project Structure
```
network_intrusion_app/
├── backend/
│   ├── app.py           # Flask backend server
│   ├── analyzer.py      # Packet analysis and ML prediction
│   ├── capture.py       # Packet capture logic
│   ├── train_model.py   # Model training script
│   ├── models/          # Saved ML models
│   └── utils.py         # Feature extraction utilities
├── dataset/
│   └── live_capture.pcap # Captured packet data
├── frontend/
│   └── index.html       # Web UI
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Setup Instructions
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/network_intrusion_app.git
   cd network_intrusion_app
   ```
2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # Or: source venv/bin/activate  # On Linux/Mac
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Install TShark:**
   - Download and install Wireshark from https://www.wireshark.org/download.html
   - Ensure `tshark` is available in your system PATH.

## Usage
### 1. Start the Backend
```sh
cd backend
python app.py
```
- The backend will start a Flask server (default: http://127.0.0.1:5000).

### 2. Start Packet Capture
- Use the web interface or backend endpoint to start capturing packets. Captured data is saved as `dataset/live_capture.pcap`.

### 3. Analyze Captured Data
- The backend will process the `.pcap` file, extract features, and predict anomalies using the trained model.

### 4. Frontend
- Open `frontend/index.html` in your browser to interact with the web UI.

### 5. Train the Model (Optional)
- To retrain the anomaly detection model:
  ```sh
  cd backend
  python train_model.py --input ../dataset/live_capture.pcap
  ```
- This will update `models/trained_model.pkl` and `feature_columns.txt`.

## Troubleshooting
- **TShark Crashes/Error code 2:**
  - Ensure the `.pcap` file is not corrupted or incomplete. Delete and re-capture if needed.
  - Verify `tshark` is correctly installed and accessible from the command line.
- **Feature Mismatch:**
  - Always retrain the model if you change feature extraction logic.
  - Ensure `feature_columns.txt` matches features used during prediction.
- **Permission Issues:**
  - Run the backend with sufficient privileges to capture packets (may require admin/root access).

## Contributing
Contributions are welcome! Please open issues or pull requests for bug fixes, improvements, or new features.

## License
This project is licensed under the MIT License.

## Acknowledgments
- [Wireshark](https://www.wireshark.org/)
- [Pyshark](https://github.com/KimiNewt/pyshark)
- [scikit-learn](https://scikit-learn.org/)

---
For questions or support, please open an issue on GitHub.

**##Screenshot**
![Image](https://github.com/user-attachments/assets/319ce669-73d3-423e-a0a8-341fabe5fd49)

