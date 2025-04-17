import os
import joblib
import pandas as pd
import utils

def analyze(pcap_path):
    print(f"[DEBUG] Starting analysis for: {pcap_path}")
    # Load model
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'trained_model.pkl')
    try:
        print(f"[DEBUG] Loading model from: {model_path}")
        model = joblib.load(model_path)
        print(f"[DEBUG] Model loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Model load failed: {e}")
        return {'error': f'Model load failed: {e}'}

    # Parse packets and extract features
    df = utils.parse_pcap(pcap_path)
    print(f"[DEBUG] DataFrame shape after parse_pcap: {df.shape}")
    if df.empty:
        print(f"[DEBUG] No packets found in pcap.")
        return {'summary': {'normal': 0, 'anomaly': 0}, 'packets': []}

    features = utils.extract_features(df)
    print(f"[DEBUG] Features shape: {features.shape}")
    # Align features to training columns
    feature_cols_path = os.path.join(os.path.dirname(__file__), 'models', 'feature_columns.txt')
    if os.path.exists(feature_cols_path):
        with open(feature_cols_path, 'r') as f:
            train_cols = [line.strip() for line in f.readlines()]
        for col in train_cols:
            if col not in features.columns:
                features[col] = 0
        features = features[train_cols]
        print(f"[DEBUG] Features aligned to training columns: {len(train_cols)} columns")
    else:
        print(f"[WARN] feature_columns.txt not found, using raw features.")
    # Predict using IsolationForest (1=inlier, -1=outlier)
    try:
        preds = model.predict(features)
        print(f"[DEBUG] Prediction complete. {len(preds)} packets analyzed.")
    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        return {'error': f'Prediction failed: {e}'}
    df['prediction'] = preds
    df['label'] = df['prediction'].apply(lambda x: 'normal' if x == 1 else 'anomaly')

    # Summarize results
    normal_count = int((df['prediction'] == 1).sum())
    anomaly_count = int((df['prediction'] == -1).sum())
    print(f"[DEBUG] Normal: {normal_count}, Anomaly: {anomaly_count}")
    packets = df.to_dict(orient='records')

    return {'summary': {'normal': normal_count, 'anomaly': anomaly_count}, 'packets': packets}
