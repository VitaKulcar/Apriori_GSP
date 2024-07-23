let months = []
let monthIndex = 0
let selectedDataset = ""
let feature = ""
let attr = ""

const buttons = document.querySelectorAll(".dataset-button")
const slider = document.getElementById("monthSlider");
const selectedDate = document.getElementById('monthLabel');

buttons.forEach(button => {
    button.addEventListener("click", function () {
        buttons.forEach(btn => btn.classList.remove("active"))
        this.classList.add("active")
        selectedDataset = this.getAttribute("data-dataset")
        getData(selectedDataset)

        fetch(`/get-csv-dates?dataset=${selectedDataset}`)
            .then(response => response.json())
            .then(data => {
                months = data.dates
                slider.max = months.length - 1;
                selectedDate.textContent = data[0];
                slider.addEventListener('change', function () {
                    monthIndex = monthSlider.value;
                    selectedDate.textContent = data[monthIndex];
                    updateGraphs(selectedDataset)
                });
            });
    });
});


function updateGraphs() {
    const selectedMonth = months[monthIndex]
    document.getElementById("monthLabel").textContent = selectedMonth

    fetch(`/get_graphs?date=${selectedMonth}&type=APRIORI&dataset=${selectedDataset}`)
        .then(response => response.json())
        .then(data => {
            if (data.error === undefined) {
                Plotly.react("aprioriSankey", JSON.parse(data.sankey).data, JSON.parse(data.sankey).layout)
                Plotly.react("aprioriWeightedGraph", JSON.parse(data.weighted_graph).data, JSON.parse(data.weighted_graph).layout)
            } else {
                Plotly.react("aprioriSankey", [], {})
                Plotly.react("aprioriWeightedGraph", [], {})
            }
        })

    fetch(`/get_graphs?date=${selectedMonth}&type=GSP&dataset=${selectedDataset}`)
        .then(response => response.json())
        .then(data => {
            if (data.error === undefined) {
                Plotly.react("gspSankey", JSON.parse(data.sankey).data, JSON.parse(data.sankey).layout)
                Plotly.react("gspWeightedGraph", JSON.parse(data.weighted_graph).data, JSON.parse(data.weighted_graph).layout)
            } else {
                Plotly.react("gspSankey", [], {})
                Plotly.react("gspWeightedGraph", [], {})
            }
        })
}

function getData() {
    console.log(selectedDataset)
    fetch(`/get_attributes?dataset=${selectedDataset}`)
        .then(response => response.json())
        .then(data => {
            if (data.error === undefined) {
                feature = JSON.parse(data.feature).data
                attr = JSON.parse(data.attr).data
            }
            refreshTable(feature, attr)
        })
}

function refreshTable(feature, attributes) {
    const tableBody = document.getElementById("attributesTableBody")
    tableBody.innerHTML = ""

    const row = document.createElement("tr")
    const featureCell = document.createElement("td")
    featureCell.textContent = feature
    row.appendChild(featureCell)

    const cell = document.createElement("td")
    cell.textContent = attributes
    row.appendChild(cell)
    tableBody.appendChild(row)
}