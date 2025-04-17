import subprocess
import signal
import os

# Global variable to store the capture process
capture_process = None

def start_capture(pcap_path, interface=None):
    global capture_process
    # Ensure any existing capture is stopped
    if capture_process:
        stop_capture()
    # Auto-detect interface if not provided
    if not interface:
        interface = detect_interface()
    if not interface:
        raise RuntimeError('No network interface detected')
    # Start tshark capture
    cmd = ['tshark', '-i', interface, '-w', pcap_path]
    print(f"Running capture: {' '.join(cmd)}")
    try:
        capture_process = subprocess.Popen(cmd)
        return capture_process.pid
    except FileNotFoundError:
        raise RuntimeError('tshark not found; ensure it is installed and in PATH')
    except Exception as e:
        raise RuntimeError(f'Failed to start capture: {e}')


def stop_capture():
    global capture_process
    if not capture_process:
        return False
    try:
        os.kill(capture_process.pid, signal.SIGINT)
        capture_process.wait()
        capture_process = None
        return True
    except Exception as e:
        print(f"Error stopping capture: {e}")
        return False


def list_interfaces():
    try:
        output = subprocess.check_output(['tshark', '-D'], stderr=subprocess.STDOUT).decode()
        interfaces = []
        for line in output.splitlines():
            if not line.strip():
                continue
            idx, name = line.split('.', 1)
            interfaces.append({'id': idx.strip(), 'name': name.strip()})
        return interfaces
    except Exception as e:
        print(f"Error listing interfaces: {e}")
        return []


def detect_interface():
    """Return the ID of the Wi-Fi or wireless interface, or first available."""
    ints = list_interfaces()
    print(f"Available interfaces: {ints}")
    # Look for Wi-Fi or wireless keywords
    for intf in ints:
        name = intf['name'].lower()
        if any(keyword in name for keyword in ['wi-fi', 'wifi', 'wlan', 'wireless']):
            print(f"Auto-selected interface: {intf['id']} ({intf['name']})")
            return intf['id']
    # Fallback to first interface
    if ints:
        print(f"No Wi-Fi found; using first interface: {ints[0]['id']} ({ints[0]['name']})")
        return ints[0]['id']
    print("No network interfaces detected")
    return None
