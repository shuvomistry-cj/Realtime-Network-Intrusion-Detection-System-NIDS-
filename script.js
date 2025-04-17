const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const statusText = document.getElementById('status');
let packetCount = 0;
let packetCountInterval = null;
const resultsSection = document.getElementById('resultsSection');
const normalCountEl = document.getElementById('normalCount');
const anomalyCountEl = document.getElementById('anomalyCount');
const packetsTable = document.getElementById('packetsTable');
const interfaceSelect = document.getElementById('interfaceSelect');

let chart;

// Load available interfaces on startup
window.addEventListener('DOMContentLoaded', () => {
  fetch('http://localhost:5000/interfaces')
    .then(res => res.json())
    .then(data => {
      data.interfaces.forEach(iface => {
        const opt = document.createElement('option');
        opt.value = iface.id;
        opt.textContent = iface.name;
        interfaceSelect.appendChild(opt);
      });
    });
});

startBtn.addEventListener('click', () => {
  packetCount = 0;
  statusText.textContent = 'Status: Capturing...';
  if (packetCountInterval) clearInterval(packetCountInterval);
  packetCountInterval = setInterval(() => {
    fetch('http://localhost:5000/packet-count')
      .then(res => res.json())
      .then(data => {
        packetCount = data.count;
        statusText.textContent = `Status: Capturing | Packets: ${packetCount}`;
      });
  }, 1000);

  fetch('http://localhost:5000/start-capture', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ interface: interfaceSelect.value })
  })
    .then(res => res.json())
    .then(data => {
      statusText.textContent = `Status: Capturing (PID: ${data.pid})`;
    });
});

stopBtn.addEventListener('click', () => {
  if (packetCountInterval) clearInterval(packetCountInterval);
  statusText.textContent = `Status: Stopped | Packets: ${packetCount}`;
  document.getElementById('analyzeBtn').classList.remove('d-none');
  fetch('http://localhost:5000/stop-capture', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
      statusText.textContent = 'Status: Stopped';
      loadResults();
    });
});

document.addEventListener('DOMContentLoaded', () => {
  // Add Analyze button
  const analyzeBtn = document.createElement('button');
  analyzeBtn.id = 'analyzeBtn';
  analyzeBtn.className = 'btn btn-primary d-none ms-2';
  analyzeBtn.textContent = 'Analyze';
  analyzeBtn.onclick = () => {
    loadResults();
    analyzeBtn.classList.add('d-none');
  };
  document.querySelector('.mb-3').appendChild(analyzeBtn);
});

function loadResults() {
  fetch('http://localhost:5000/results')
    .then(res => res.json())
    .then(data => {
      const results = data.results;
      normalCountEl.textContent = results.summary.normal;
      anomalyCountEl.textContent = results.summary.anomaly;
      renderChart(results.summary);
      populateTable(results.packets);
      resultsSection.classList.remove('d-none');
      // Show anomaly percentage
      const total = results.summary.normal + results.summary.anomaly;
      let percent = total ? ((results.summary.anomaly / total) * 100).toFixed(2) : 0;
      let msg = '';
      if (total === 0) {
        msg = 'No packets captured.';
      } else if (results.summary.anomaly === 0) {
        msg = 'No anomalies detected.';
      } else {
        msg = `Anomaly rate: ${percent}% (${results.summary.anomaly} of ${total} packets)`;
      }
      let summaryMsg = document.getElementById('summaryMsg');
      if (!summaryMsg) {
        summaryMsg = document.createElement('div');
        summaryMsg.id = 'summaryMsg';
        summaryMsg.className = 'mt-2 fw-bold';
        resultsSection.insertBefore(summaryMsg, resultsSection.children[1]);
      }
      summaryMsg.textContent = msg;
    });
}

function renderChart(summary) {
  const ctx = document.getElementById('chart').getContext('2d');
  if (chart) chart.destroy();
  chart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Normal', 'Anomaly'],
      datasets: [{ data: [summary.normal, summary.anomaly], backgroundColor: ['#28a745', '#dc3545'] }]
    }
  });
}

function populateTable(packets) {
  packetsTable.innerHTML = '';
  packets.forEach(pkt => {
    if (pkt.label === 'anomaly') {
      const row = document.createElement('tr');
      row.innerHTML = `<td>${new Date(pkt.timestamp * 1000).toLocaleTimeString()}</td><td>${pkt.protocol}</td><td>${pkt.length}</td><td>${pkt.label}</td>`;
      packetsTable.appendChild(row);
    }
  });
}
