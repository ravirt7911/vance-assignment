const ctx = document.getElementById('exchangeRateChart').getContext('2d');
let exchangeRateChart;

// Function to fetch data from the API based on the selected period and currency pair
function fetchData(period, fromCurrency, toCurrency) {
    const url = `http://localhost:5006/api/forex-data?from=${fromCurrency}&to=${toCurrency}&period=${period}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const labels = data.map(entry => new Date(entry.Date).toLocaleDateString());
            const prices = data.map(entry => entry.Close);
            renderChart(labels, prices); 
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

// Function to render the chart using Chart.js
function renderChart(labels, prices) {
    if (exchangeRateChart) {
        exchangeRateChart.destroy(); 
    }

    exchangeRateChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `Exchange Rate (${currentFromCurrency} to ${currentToCurrency})`,
                data: prices,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                tension: 0.1 
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Date' } },
                y: { title: { display: true, text: 'Exchange Rate' } }
            }
        }
    });
}

// Initial currency settings
let currentFromCurrency = 'GBP';
let currentToCurrency = 'INR';

// Fetch initial data for the default period (1M)
fetchData('1M', currentFromCurrency, currentToCurrency);

// Event listeners for currency selection
document.getElementById('currencySelector').addEventListener('change', function() {
    const selectedCurrencyPair = this.value.split('-');
    currentFromCurrency = selectedCurrencyPair[0];
    currentToCurrency = selectedCurrencyPair[1];
    
    // Fetch initial data for the selected currency pair and default period (1M)
    fetchData('1M', currentFromCurrency, currentToCurrency);
});

// Event listeners for buttons
document.querySelectorAll('.period-button').forEach(button => {
    button.addEventListener('click', function() {
        const selectedPeriod = this.dataset.period;
        fetchData(selectedPeriod, currentFromCurrency, currentToCurrency);
    });
});