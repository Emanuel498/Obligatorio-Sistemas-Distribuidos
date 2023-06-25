const labels = []
const cantAlerts = []

fetch("http://localhost:8080/api/datos")
    .then(response => response.json())
    .then(data => {
        data.forEach(element => {
            labels.push(element["location"])
            cantAlerts.push(element["cantidad"])
        });

        // Manipular los datos recibidos y generar la gráfica
        // Puedes utilizar una biblioteca como Chart.js para generar la gráfica en base a los datos obtenidos
    })
    .catch(error => {
        console.error('Error:', error);
    });

const dataset = {
    label: "Dataset 1",
    data: cantAlerts,
    borderColor: 'rgba(248, 37, 37, 0.8)',
    fill: false,
    tension: 0.1
};


const graph = document.querySelector("#grafica");

const data = {
    labels: labels,
    datasets: dataset
};

const config = {
    type: 'line',
    data: data,
};

new Chart(graph, config);