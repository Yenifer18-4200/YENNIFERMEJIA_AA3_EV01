
// Use a relative path to avoid CORS restrictions and port issues.
const API_BASE_URL = window.location.origin;

document.addEventListener("DOMContentLoaded", () => {
    // Initialize modules based on the elements present in the DOM.
    if (document.getElementById("products-table-body")) {
        loadProducts();
    }
    if (document.getElementById("orders-table-body")) {
        loadOrders();
    }
    if (document.getElementById("product-form")) {
        setupProductForm();
    }
});

/**
 * Module 1: Load product catalog (FR3 - Data Presentation).
 */
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products`);
        if (!response.ok) throw new Error("Failed to retrieve products");

        const products = await response.json();
        const tableBody = document.getElementById("products-table-body");

        if (!tableBody) return;
        tableBody.innerHTML = "";

        products.forEach(product => {
            const row = document.createElement("tr");

            // Validate that values are available.
            const id = product.id || product.product_id || "-";
            const name = product.name || product.product_name || "No name";
            const price = product.price ? parseFloat(product.price).toFixed(2) : "0.00";
            const stock = product.stock !== undefined ? product.stock : 0;

            row.innerHTML = `
                <td>#${id}</td>
                <td><strong>${name}</strong></td>
                <td>$${price}</td>
                <td><span class="badge ${stock > 5 ? 'bg-success' : 'bg-warning'}">${stock} units</span></td>
                <td>
                    <button class="btn-sm btn-delete" onclick="deleteProduct(${id})">Delete</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error connecting to the backend:", error);
        showNotification("Could not load the product inventory.", "error");
    }
}

/**
 * Module 2: Register new products (FR2 - Inventory Ingestion).
 */
function setupProductForm() {
    const form = document.getElementById("product-form");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const nameInput = document.getElementById("product-name");
        const priceInput = document.getElementById("product-price");
        const stockInput = document.getElementById("product-stock");

        if (!nameInput || !priceInput || !stockInput) return;

        const newProduct = {
            name: nameInput.value.toLowerCase().trim(),
            price: parseFloat(priceInput.value),
            stock: parseInt(stockInput.value, 10)
        };

        try {
            const response = await fetch(`${API_BASE_URL}/products`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(newProduct)
            });

            if (response.ok) {
                showNotification("Product registered successfully", "success");
                form.reset();
                if (document.getElementById("products-table-body")) {
                    loadProducts();
                }
            } else {
                const errorData = await response.json();
                const errorMsg = errorData.detail ? JSON.stringify(errorData.detail) : "Form error";
                showNotification(`Validation error: ${errorMsg}`, "error");
            }
        } catch (error) {
            console.error("Error in POST request:", error);
            showNotification("Connection error while saving the product.", "error");
        }
    });
}

/**
 * Module 3: Delete products (FR6 - Administrative CRUD).
 */
async function deleteProduct(productId) {
    if (!confirm(`Are you sure you want to delete product #${productId}?`)) return;

    try {
        const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
            method: "DELETE"
        });

        if (response.ok) {
            showNotification("Product successfully deleted.", "success");
            loadProducts();
        } else {
            showNotification("Could not delete the specified product.", "error");
        }
    } catch (error) {
        console.error("Error in DELETE request:", error);
        showNotification("Server error while attempting to delete the product.", "error");
    }
}

/**
 * Module 4: Load invoices and orders (FR7 - Business Intelligence).
 */
async function loadOrders() {
    try {
        const response = await fetch(`${API_BASE_URL}/orders`);
        const data = await response.json();

        // Handle responses returned as either a list ([]) or an object ({ orders: [] }).
        const orders = Array.isArray(data) ? data : (data.orders || []);

        const tableBody = document.getElementById('orders-table-body');
        if (!tableBody) return;

        tableBody.innerHTML = '';

        orders.forEach(order => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>#${order.id || order.order_id || ''}</td>
                <td>${order.customer_name || order.user_id || 'Customer'}</td>
                <td>$${parseFloat(order.total_amount || order.total || 0).toFixed(2)}</td>
                <td><span class="badge bg-success">${order.status || 'Completed'}</span></td>
            `;
            tableBody.appendChild(row);
        });

        // Update the orders counter if it exists.
        const ordersCount = document.getElementById('orders-count');
        if (ordersCount) {
            ordersCount.textContent = orders.length;
        }

    } catch (error) {
        console.error('Error loading orders:', error);
        showNotification("Error loading the orders list.", "error");
    }
}

/**
 * UI component: Visual notification feedback.
 */
function showNotification(message, type = "info") {
    const alertBox = document.getElementById("ui-notification");
    if (!alertBox) {
        alert(message);
        return;
    }
    alertBox.textContent = message;
    alertBox.className = `notification-toast toast-${type} active`;

    setTimeout(() => {
        alertBox.classList.remove("active");
    }, 4000);
}
