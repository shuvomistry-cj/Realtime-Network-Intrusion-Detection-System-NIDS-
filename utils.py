import pyshark
import pandas as pd

def parse_pcap(pcap_path):
    try:
        cap = pyshark.FileCapture(pcap_path, keep_packets=False)
        packets = []
        for pkt in cap:
            try:
                packets.append({
                    'timestamp': float(pkt.sniff_timestamp),
                    'protocol': pkt.highest_layer,
                    'length': int(pkt.length)
                })
            except AttributeError:
                continue
        cap.close()
        return pd.DataFrame(packets)
    except Exception as e:
        print(f"Error parsing pcap: {e}")
        return pd.DataFrame()

import subprocess

def count_packets(pcap_path):
    try:
        # Use tshark CLI for robust counting
        output = subprocess.check_output([
            'tshark', '-r', pcap_path, '-q', '-z', 'io,phs'
        ], stderr=subprocess.STDOUT).decode(errors='ignore')
        # Look for packet count in output
        for line in output.splitlines():
            if line.strip().startswith('Total '):
                parts = line.strip().split()
                if parts[-1].isdigit():
                    return int(parts[-1])
        # Fallback: count lines with pyshark
        import pyshark
        cap = pyshark.FileCapture(pcap_path, keep_packets=False)
        count = sum(1 for _ in cap)
        cap.close()
        return count
    except Exception as e:
        print(f"Error counting packets: {e}")
        return 0

def extract_features(df):
    # Example feature engineering
    df = df.copy()
    df['time_delta'] = df['timestamp'].diff().fillna(0)
    # One-hot encode protocol
    protocols = pd.get_dummies(df['protocol'], prefix='proto')
    features = pd.concat([df[['length', 'time_delta']], protocols], axis=1)
    return features
