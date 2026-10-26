(function () {
    const data = window.AGRISENSE_DATA || {};

    const green = "#0c9858";
    const paleGreen = "rgba(12, 152, 88, 0.13)";

    Chart.defaults.font.family = "'DM Sans', Arial, sans-serif";
    Chart.defaults.color = "#718079";

    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: "#123d2b",
                padding: 11,
                cornerRadius: 8
            }
        }
    };

    // Line chart: detections over the last seven days
    const activityCanvas = document.getElementById("activityChart");

    if (activityCanvas) {
        new Chart(activityCanvas, {
            type: "line",
            data: {
                labels: data.labels || [],
                datasets: [{
                    label: "Detections",
                    data: data.daily || [],
                    borderColor: green,
                    backgroundColor: paleGreen,
                    fill: true,
                    tension: 0.38,
                    borderWidth: 2.5,
                    pointRadius: 3,
                    pointBackgroundColor: "#fff",
                    pointBorderColor: green
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { maxRotation: 0 }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: "#edf2ee" },
                        ticks: { precision: 0 }
                    }
                }
            }
        });
    }

    // Doughnut chart: detection classes
    const classCanvas = document.getElementById("classChart");

    if (classCanvas) {
        new Chart(classCanvas, {
            type: "doughnut",
            data: {
                labels: data.classes || [],
                datasets: [{
                    data: data.classCounts || [],
                    backgroundColor: [
                        "#15995a",
                        "#24a7d6",
                        "#f1b43d",
                        "#8e70d6",
                        "#ec7e65"
                    ],
                    borderWidth: 3,
                    borderColor: "#fff",
                    hoverOffset: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "67%",
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            boxWidth: 9,
                            usePointStyle: true,
                            padding: 12
                        }
                    }
                }
            }
        });
    }

    // Bar chart: production predictions by year
    const productionCanvas = document.getElementById("productionChart");

    if (productionCanvas) {
        new Chart(productionCanvas, {
            type: "bar",
            data: {
                labels: data.years || [],
                datasets: [{
                    label: "Predictions",
                    data: data.yearCounts || [],
                    backgroundColor: "#eab63d",
                    hoverBackgroundColor: green,
                    borderRadius: 5,
                    maxBarThickness: 24
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    x: {
                        grid: { display: false }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: "#edf2ee" },
                        ticks: { precision: 0 }
                    }
                }
            }
        });
    }

    // Dashboard search
    const searchInput = document.getElementById("dashboardSearch");

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = this.value.toLowerCase().trim();

            document.querySelectorAll(".searchable").forEach(function (section) {
                const matches = section.innerText.toLowerCase().includes(query);
                section.classList.toggle("hidden-by-search", query && !matches);
            });
        });
    }
})();