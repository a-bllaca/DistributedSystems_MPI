from flask import Flask, jsonify, render_template_string
import pandas as pd
import os
from pathlib import Path

app = Flask(__name__)
output_dir = Path("/data/worker_outputs")

@app.route("/api/results", methods=["GET"])
def get_aggregated_results():
    all_data = []

    for csv_file in output_dir.glob("*.csv"):
        try:
            df = pd.read_csv(csv_file)
            all_data.append(df)
        except Exception as e:
            print(f"Failed to read {csv_file}: {e}")

    if not all_data:
        return jsonify([])

    merged_df = pd.concat(all_data, ignore_index=True)

    # 🧠 GROUP and AVERAGE by device_id
    aggregated = merged_df.groupby("device_id").agg({
        "mean_temperature": "mean",
        "mean_pressure": "mean",
        "mean_voltage": "mean",
        "mean_current": "mean",
        "num_readings": "sum"
    }).reset_index()

    return aggregated.to_json(orient="records")

@app.route("/")
def home():
    return render_template_string('''
   <!DOCTYPE html>
<html>
<head>
    <title>Sensor Feature Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>Aggregated Sensor Data</h1>
    <button onclick="createCharts()">Reload Charts</button>
    <div>
        <canvas id="temperatureChart" width="600" height="400"></canvas>
    </div>
    <div>
        <canvas id="pressureChart" width="600" height="400"></canvas>
    </div>
    <div>
        <canvas id="readingsChart" width="600" height="400"></canvas>
    </div>
    <script>
        async function fetchData() {
            const response = await fetch('/api/results');
            const data = await response.json();
            return data;
        }

        function prepareChartData(data, feature) {
            const labels = data.map(d => d.device_id);
            const values = data.map(d => d[feature]);
            return { labels, values };
        }

        async function createCharts() {
            const data = await fetchData();

            const tempData = prepareChartData(data, "mean_temperature");
            const pressureData = prepareChartData(data, "mean_pressure");
            const readingsData = prepareChartData(data, "num_readings");

            // 🎯 Temperature chart
            new Chart(document.getElementById('temperatureChart'), {
                type: 'bar',
                data: {
                    labels: tempData.labels,
                    datasets: [{
                        label: 'Avg Temperature (°C)',
                        data: tempData.values,
                        backgroundColor: tempData.values.map(v => v > 80 ? 'rgba(255,0,0,0.7)' : 'rgba(255,99,132,0.6)') // RED if > 80°C
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' }
                    }
                }
            });

            // 🎯 Pressure chart
            new Chart(document.getElementById('pressureChart'), {
                type: 'bar',
                data: {
                    labels: pressureData.labels,
                    datasets: [{
                        label: 'Avg Pressure (bar)',
                        data: pressureData.values,
                        backgroundColor: pressureData.values.map(v => v > 4 ? 'rgba(255,165,0,0.7)' : 'rgba(54,162,235,0.6)') // ORANGE if > 4 bar
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' }
                    }
                }
            });

            // 🎯 Total readings chart
            new Chart(document.getElementById('readingsChart'), {
                type: 'bar',
                data: {
                    labels: readingsData.labels,
                    datasets: [{
                        label: 'Total Readings',
                        data: readingsData.values,
                        backgroundColor: 'rgba(75,192,192,0.6)'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' }
                    }
                }
            });
        }

        createCharts();
    </script>
</body>
</html>

    ''')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
