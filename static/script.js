document.addEventListener('DOMContentLoaded', () => {
    const watchlist = document.getElementById('watchlist');
    const searchInput = document.getElementById('search');
    const stockTableBody = document.querySelector('#stock-table tbody');

    let watchlistStocks = [];
    let allStocks = [];

    // Fetch data and initialize the app
    Promise.all([fetchAllStocks(), fetchWatchlist()])
        .then(() => {
            displayStockTable(allStocks);
            updateWatchlist();
        });

    // Fetch all stocks from the API
    async function fetchAllStocks() {
        try {
            const response = await fetch('https://integral-christa-keesha-2df2a8e4.koyeb.app/stocks_list');
            const data = await response.json();
            if (data && data.response && data.response.stock_list) {
                allStocks = data.response.stock_list;
            } else {
                console.error('Invalid data structure:', data);
            }
        } catch (error) {
            return console.error('Error fetching all stocks:', error);
        }
    }

    // Fetch watchlist from the API
    async function fetchWatchlist() {
        try {
            const response = await fetch('https://integral-christa-keesha-2df2a8e4.koyeb.app/dashboard_stock');
            const data = await response.json();
            if (data && data.response && data.response.stock_list) {
                watchlistStocks = data.response.stock_list;
            } else {
                console.error('Invalid data structure:', data);
            }
        } catch (error) {
            return console.error('Error fetching watchlist:', error);
        }
    }


    function updateWatchlist() {
        // Clear previous items
        watchlist.innerHTML = '';
        watchlistStocks
            .forEach((stock) => {
                const li = document.createElement('li');
                li.textContent = `${stock.stock_name} (${stock.stock_ticker}) `;
                const removeButton = document.createElement('button');
                removeButton.textContent = 'Remove';
                removeButton.classList.add('remove');
                removeButton
                    .addEventListener('click', () => {
                        watchlistStocks = watchlistStocks.filter(item => item.stock_ticker !== stock.stock_ticker);
                        removeWatchListStock(stock.stock_ticker);
                    });
                li.appendChild(removeButton);
                watchlist.appendChild(li);
            });
    }


    function displayStockTable(stocks) {
        // Clear previous data
        stockTableBody.innerHTML = '';
        stocks.forEach((stock) => {
            //const changeClass = stock.change >= 0 ? 'positive' : 'negative';
            const tr = document.createElement('tr');
            tr.innerHTML = `
            <td>${stock.stock_name}</td>
            <td class="actions"></td>
        `;
            const actionsTd = tr.querySelector('.actions');

            if (!watchlistStocks.some(item => item.stock_ticker === stock.stock_ticker)) {
                const addButton = document.createElement('button');
                addButton.textContent = 'Add';
                addButton.classList.add('add');
                addButton.addEventListener('click', () => {
                    watchlistStocks.push(stock);
                    addWatchListStock(stock)
                });
                actionsTd.appendChild(addButton);
            } else {
                const removeButton = document.createElement('button');
                removeButton.textContent = 'Remove';
                removeButton.classList.add('remove');
                removeButton
                    .addEventListener('click', () => {
                        watchlistStocks = watchlistStocks.filter(item => item.stock_ticker !== stock.stock_ticker);
                        removeWatchListStock(stock.stock_ticker);
                    });
                actionsTd.appendChild(removeButton);
            }

            // Add event listener to display
            //  stock details when clicked
            tr.addEventListener('click', () => {
                //displayStockInfo(stock);
            });
            stockTableBody.appendChild(tr);
        });
    }

    searchInput
        .addEventListener('input', (event) => {
            const searchTerm = event.target.value.toLowerCase();
            const filteredStocks = allStocks
                .filter(stock => stock.stock_name.toLowerCase().includes(searchTerm) ||
                    stock.stock_ticker.toLowerCase().includes(searchTerm));
            displayStockTable(filteredStocks);
        });


    function addWatchListStock(stock) {
        try {
            const requestBody = JSON.stringify({ stock_ticker: stock.stock_ticker, stock_name: stock.stock_name });
            const response = fetch('https://integral-christa-keesha-2df2a8e4.koyeb.app/add_stock',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: requestBody
                });
            const data = response.json();
            if (data && data.response && data.response.stock_added) {
                stockAdded = data.response.stock_added;
                // Refresh the table's to update the "Add/Remove" buttons
                updateWatchlist();
                displayStockTable(allStocks);
            } else {
                console.error('Invalid data structure:', data);
                // Refresh the table's to update the "Add/Remove" buttons
                updateWatchlist();
                displayStockTable(allStocks);
            }
        } catch (error) {
            // Refresh the table's to update the "Add/Remove" buttons
            updateWatchlist();
            displayStockTable(allStocks);
            return console.error('Error adding stock to watchlist:', error);
        }
    }

    function removeWatchListStock(stock_ticker) {
        try {
            const requestBody = JSON.stringify({ stock_ticker: stock_ticker });
            const response = fetch('https://integral-christa-keesha-2df2a8e4.koyeb.app/remove_stock',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: requestBody
                });
            const data = response.json();
            if (data && data.response && data.response.stock_removed) {
                stockRemoved = data.response.stock_removed;
                // Refresh the table's to update the "Add/Remove" buttons
                updateWatchlist();
                displayStockTable(allStocks);
            } else {
                console.error('Invalid data structure:', data);
                // Refresh the table's to update the "Add/Remove" buttons
                updateWatchlist();
                displayStockTable(allStocks);
            }
        } catch (error) {
            // Refresh the table's to update the "Add/Remove" buttons
            updateWatchlist();
            displayStockTable(allStocks);
            return console.error('Error removing stock from watchlist:', error);
        }
    }
});