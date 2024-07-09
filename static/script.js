document.addEventListener('DOMContentLoaded', () => {
    const refreshButton = document.getElementById('refresh-button');
    const watchlistTableBody = document.querySelector('#watchlist-table tbody');
    const searchInput = document.getElementById('search');
    const stockTableBody = document.querySelector('#stock-table tbody');
    const loaderItem = document.getElementById('loader');
    const refreshTime = document.getElementById('refresh-time');
    const addStock = document.getElementById('add-stock-button');
    const addStockDialog = document.getElementById('add_stock_dialog');
    const cancelDialogBtn = document.getElementById('cancel-dialog-btn');
    const addStockDialogForm = document.getElementById('add_stock_dialog_form');


    const base_url = ''
    //const base_url = 'https://tender-nightingale-keesha-36143a60.koyeb.app'
    //const base_url = 'https://stockanalyserengine.onrender.com'
    //const base_url = 'http://127.0.0.1:5000'

    let watchlistStocks = [];
    let allStocks = [];

    function loader(visibility) {
        if (visibility == "show") {
            loaderItem.style.visibility = 'visible';
        } else
            loaderItem.style.visibility = 'hidden';
    }
    //Handle refresh button
    refreshButton.addEventListener('click', () => {
        loader("show")
        updateWatchlistStockData()
    });

    // Fetch data and initialize the app
    Promise.all([fetchAllStocks(), fetchWatchlist()])
        .then(() => {
            displayStockTable(allStocks);
            updateWatchlistStockData();
        });

    // Fetch all stocks from the API
    async function fetchAllStocks() {
        loader("show")
        try {
            const url = `${base_url}/stocks_list`;
            const response = await fetch(url);
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
        loader("show")
        try {
            const url = `${base_url}/dashboard_stock`;
            const response = await fetch(url);
            const data = await response.json();
            if (data && data.response && data.response.stock_list) {
                watchlistStocks = data.response.stock_list;
                updateWatchlist();
            } else {
                console.error('Invalid data structure:', data);
            }
        } catch (error) {
            return console.error('Error fetching watchlist:', error);
        }
    }

    async function updateWatchlistStockData() {
        loader("show")
        const url_52weekhigh = `${base_url}/difference_from_52_week_high`;
        const fetchPromises = watchlistStocks.map(async (stock) => {
            try {
                const params = { stock_ticker: stock.stock_ticker };
                const queryString = new URLSearchParams(params).toString();
                const urlWithParams = `${url_52weekhigh}?${queryString}`;
                const response = await fetch(urlWithParams);
                const data = await response.json();
                if (data && data.response && data.response.percentage_diff_from_52_week_high && data.response.updated_at) {
                    updateSuccessful = data.response.updateSuccessful;
                    refreshTime.textContent = `Last refreshed at - ${data.response.updated_at}`
                } else {
                    console.error('Invalid data structure:', data);
                }
            } catch (error) {
                console.error('Error fetching 52_week_high value:', error);
            }
        });
        await Promise.all(fetchPromises);
        fetchWatchlist();

    }

    function updateWatchlist() {
        // Clear previous items
        watchlistTableBody.innerHTML = '';
        watchlistStocks.forEach((stock) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${stock.stock_name}(${stock.stock_ticker})</td>
                <td>${stock.current_value}</td>
                <td>${stock.percentage_from_52week_high}%</td>
                `;
            // const removeButton = document.createElement('button');
            // removeButton.textContent = 'Remove';
            // removeButton.classList.add('remove');
            // removeButton
            //     .addEventListener('click', () => {
            //         watchlistStocks = watchlistStocks.filter(item => item.stock_ticker !== stock.stock_ticker);
            //         removeWatchListStock(stock.stock_ticker);
            //     });
            // tr.appendChild(removeButton);
            watchlistTableBody.appendChild(tr);
        });
        loader("hide")
    }


    function displayStockTable(stocks) {
        // Clear previous data
        stockTableBody.innerHTML = '';
        stocks.forEach((stock) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${stock.stock_name}</td><td class="actions"></td>`;
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
            // Add event listener to display stock details when clicked
            tr.addEventListener('click', () => {
                //displayStockInfo(stock);
            });
            stockTableBody.appendChild(tr);
        });
        loader("hide")
    }

    searchInput
        .addEventListener('input', (event) => {
            const searchTerm = event.target.value.toLowerCase();
            const filteredStocks = allStocks
                .filter(stock => stock.stock_name.toLowerCase().includes(searchTerm) ||
                    stock.stock_ticker.toLowerCase().includes(searchTerm));
            displayStockTable(filteredStocks);
        });

    //Handle add stock button
    addStock.addEventListener('click', () => {
        addStockDialog.showModal();
    });

    //Handle cancel dialog button
    cancelDialogBtn.addEventListener('click', () => {
        addStockDialog.close();
    });

    addStockDialogForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the form from submitting the traditional way
        const fieldStockTicker = document.getElementById('stock_ticker').value;
        const fieldStockName = document.getElementById('stock_name').value;
        addNewStockToDb(fieldStockTicker, fieldStockName)
        addStockDialog.close(); // Close the dialog
    });


    async function addWatchListStock(stock) {
        loader("show")
        try {
            const requestBody = JSON.stringify({ stock_ticker: stock.stock_ticker, stock_name: stock.stock_name });
            const url = `${base_url}/add_stock`;
            const response = await fetch(url,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: requestBody
                });
            const data = await response.json();
            if (data && data.response && data.response.stock_added) {
                stockAdded = data.response.stock_added;
                updateWatchlistStockData()
                searchInput.value = ''
                displayStockTable(allStocks);
            } else {
                console.error('Invalid data structure:', data);
            }
        } catch (error) {
            return console.error('Error adding stock to watchlist:', error);
        }
    }

    async function removeWatchListStock(stock_ticker) {
        loader("show")
        try {
            const requestBody = JSON.stringify({ stock_ticker: stock_ticker });
            const url = `${base_url}/remove_stock`;
            const response = await fetch(url,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: requestBody
                });
            const data = await response.json();
            if (data && data.response && data.response.stock_removed) {
                stockRemoved = data.response.stock_removed;
                updateWatchlist();
                searchInput.value = ''
                displayStockTable(allStocks);
            } else {
                console.error('Invalid data structure:', data);
            }
        } catch (error) {
            return console.error('Error removing stock from watchlist:', error);
        }
    }

    async function addNewStockToDb(stockTicker, stockName) {
        loader("show")
        try {
            const requestBody = JSON.stringify({ stock_ticker: stockTicker, stock_name: stockName });
            const url = `${base_url}/add_new_stock`;
            const response = await fetch(url,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: requestBody
                });
            const data = await response.json();
            if (data && data.response && data.response.stock_added) {
                stockAdded = data.response.stock_added;
                fetchAllStocks()
                alert("Stock added successfully.");
                loader("hide")
            } else {
                console.error('Invalid data structure:', data);
                loader("hide")
                if(data.status && data.status.message)
                    alert(data.status.message);
                else
                    alert("Stock added successfully.");
            }
        } catch (error) {
            loader("hide")
            return console.error('Error removing stock from watchlist:', error);
        }
    }
});