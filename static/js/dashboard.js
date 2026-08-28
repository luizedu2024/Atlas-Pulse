const labels = JSON.parse(document.getElementById("chart-labels").textContent);
const values = JSON.parse(document.getElementById("chart-values").textContent);
const canvas = document.getElementById("telemetryChart");
if (canvas) {
  new Chart(canvas, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Temperature C",
        data: values,
        borderColor: "#38bdf8",
        backgroundColor: "rgba(56,189,248,.14)",
        fill: true,
        tension: .35
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#cbd5e1" } } },
      scales: {
        x: { ticks: { color: "#94a3b8" }, grid: { color: "#243148" } },
        y: { ticks: { color: "#94a3b8" }, grid: { color: "#243148" } }
      }
    }
  });
}
