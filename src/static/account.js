document.addEventListener('DOMContentLoaded', function() {
    // Fetch strategies and positions on page load
    fetchStrategies();
    fetchPositions("BTCUSDT");

    // Event listeners for buttons
    document.getElementById('startButton').addEventListener('click', function() {
        const selectedStrategy = document.getElementById('strategySelector').value;
        startStrategy(selectedStrategy);
    });

    document.getElementById('stopButton').addEventListener('click', function() {
        stopStrategy();
    });
});

function fetchPositions(symbol) {
    fetch(`/account/positions/${symbol}`)
    .then(response => response.json())
    .then(data => {
        if (data && Array.isArray(data.list)) {
            if (data.list.length > 0) {
                updatePositionsTable(data.list);
            } else {
                document.getElementById('positions-table-body').innerHTML = '<tr><td colspan="10">No open positions</td></tr>';
            }
        } else {
            console.error('Unexpected data structure:', data);
        }
    })
    .catch(error => console.error('Error fetching positions:', error));
}

function updatePositionsTable(positions) {
    const tableBody = document.getElementById('positions-table-body');
    tableBody.innerHTML = '';

    positions.forEach(position => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${position.id || 'N/A'}</td>
            <td>${position.symbol || 'N/A'}</td>
            <td>${position.size || 'N/A'}</td>
            <td>${position.leverage || 'N/A'}</td>
            <td>${position.avgPrice || 'N/A'}</td>
            <td>${position.markPrice || 'N/A'}</td>
            <td>${position.side || 'N/A'}</td>
            <td>${position.stopLoss || 'N/A'}</td>
            <td>${position.takeProfit || 'N/A'}</td>
            <td>${position.unrealisedPnl || 'N/A'}</td>
        `;
        tableBody.appendChild(row);
    });
}

function fetchStrategies() {
    fetch('/account/strategies')
    .then(response => {
        if (!response.ok) {
            console.error('Failed to fetch strategies:', response.statusText);
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(strategies => {
        console.log('Received strategies:', strategies); // Log the strategies for debugging
        const selector = document.getElementById('strategySelector');
        strategies.forEach(strategy => {
            let option = new Option(strategy.name, strategy.name);
            selector.appendChild(option); // Add new option
        });
    })
    .catch(error => {
        console.error('Error fetching strategies:', error);
    });
}

function startStrategy(strategyName) {
    fetch(`/account/start_strategy`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ strategy: strategyName })
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to start strategy');
        alert('Strategy started successfully');
    })
    .catch(error => alert('Error starting strategy: ' + error.message));
}

function stopStrategy() {
    fetch('/account/stop_strategy', { method: 'POST' })
    .then(response => {
        if (!response.ok) throw new Error('Failed to stop strategy');
        alert('Strategy stopped successfully');
    })
    .catch(error => alert('Error stopping strategy: ' + error.message));
}
document.getElementById('closeAllPositionsButton').addEventListener('click', function() {
    closeAllPositions();
});

function closeAllPositions() {
    const symbol = "BTCUSDT"; // This should be dynamic if you support multiple symbols
    fetch('/account/close_positions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ symbol: symbol }) // Send the symbol in the body
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to close positions');
        return response.json();
    })
    .then(result => {
        alert(result.message); // Show the result message
    })
    .catch(error => alert('Error closing positions: ' + error.message));
}
