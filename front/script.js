const locations = []
const numberAlerts = []

fetch("http://localhost:8080/api/datos")
    .then(response => response.json())
    .then(data => {
        data.forEach(element => {
            locations.push(element["location"])
            numberAlerts.push(element["cantidad"])
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });

const dataset = {
    label: "Numero de alertas",
    data: numberAlerts,
    borderColor: 'rgba(248, 37, 37, 0.8)',
    fill: false,
    tension: 0.1
};

const graph = document.querySelector("#grafica");

const data = {
    labels: locations,
    datasets: dataset
};

const config = {
    type: 'line',
    data: data,
};

new Chart(graph, config);