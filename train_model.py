import os
import joblib
from sklearn.ensemble import IsolationForest
import utils

# Path to a real pcap file (should contain real traffic, captured by your app)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PCAP_PATH = os.path.join(BASE_DIR, 'dataset', 'live_capture.pcap')

print(f"[TRAIN] Extracting features from: {PCAP_PATH}")
df = utils.parse_pcap(PCAP_PATH)
if df.empty:
    raise ValueError("No packets found in the provided pcap file. Capture some traffic first!")
features = utils.extract_features(df)
print(f"[TRAIN] Features shape: {features.shape}")

# Train IsolationForest on real features
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(features)

# Save the model
model_dir = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, 'trained_model.pkl')
joblib.dump(model, model_path)
# Save feature columns
feature_cols_path = os.path.join(model_dir, 'feature_columns.txt')
with open(feature_cols_path, 'w') as f:
    for col in features.columns:
        f.write(col + '\n')
print(f"Model trained and saved to {model_path}")
print(f"Feature columns saved to {feature_cols_path}")
