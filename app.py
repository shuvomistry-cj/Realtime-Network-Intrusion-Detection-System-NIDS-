import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import capture
import analyzer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PCAP_PATH = os.path.join(BASE_DIR, 'dataset', 'live_capture.pcap')

app = Flask(__name__)
CORS(app)

@app.route('/start-capture', methods=['POST'])
def start_capture_route():
    try:
        pid = capture.start_capture(PCAP_PATH)
        return jsonify({'status': 'capturing', 'pid': pid})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/interfaces', methods=['GET'])
def interfaces_route():
    interfaces = capture.list_interfaces()
    return jsonify({'interfaces': interfaces})

@app.route('/packet-count', methods=['GET'])
def packet_count_route():
    from utils import count_packets
    count = count_packets(PCAP_PATH)
    return jsonify({'count': count})

@app.route('/stop-capture', methods=['POST'])
def stop_capture_route():
    success = capture.stop_capture()
    if not success:
        return jsonify({'status': 'error', 'message': 'No capture running'}), 400
    return jsonify({'status': 'stopped'})

@app.route('/results', methods=['GET'])
def results_route():
    results = analyzer.analyze(PCAP_PATH)
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
