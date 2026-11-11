// Usar ruta relativa para evitar bloqueos de CORS y problemas de puerto
const API_BASE_URL = window.location.origin;

document.addEventListener("DOMContentLoaded", () => {
    // Inicialización de módulos según los elementos presentes en el DOM
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
 * Módulo 1: Cargar catálogo de productos (FR3 - Data Presentation)
 */
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products`);
        if (!response.ok) throw new Error("Error al obtener los productos");

        const products = await response.json();
        const tableBody = document.getElementById("products-table-body");
        
        if (!tableBody) return;
        tableBody.innerHTML = "";

        products.forEach(product => {
            const row = document.createElement("tr");
            
            // Validaciones para asegurar que los valores existan
            const id = product.id || product.product_id || "-";
            const name = product.name || product.product_name || "Sin nombre";
            const price = product.price ? parseFloat(product.price).toFixed(2) : "0.00";
            const stock = product.stock !== undefined ? product.stock : 0;

            row.innerHTML = `
                <td>#${id}</td>
                <td><strong>${name}</strong></td>
                <td>$${price}</td>
                <td><span class="badge ${stock > 5 ? 'bg-success' : 'bg-warning'}">${stock} uds</span></td>
                <td>
                    <button class="btn-sm btn-delete" onclick="deleteProduct(${id})">Eliminar</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error conectando con el Backend:", error);
        showNotification("No se pudo cargar el inventario de productos.", "error");
    }
}

/**
 * Módulo 2: Registro de nuevos productos (FR2 - Inventory Ingestion)
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
                showNotification("Producto registrado exitosamente", "success");
                form.reset();
                if (document.getElementById("products-table-body")) {
                    loadProducts();
                }
            } else {
                const errorData = await response.json();
                const errorMsg = errorData.detail ? JSON.stringify(errorData.detail) : "Error en el formulario";
                showNotification(`Error de validación: ${errorMsg}`, "error");
            }
        } catch (error) {
            console.error("Error en la petición POST:", error);
            showNotification("Error de conexión al guardar el producto.", "error");
        }
    });
}

/**
 * Módulo 3: Eliminación de productos (FR6 - Administrative CRUD)
 */
async function deleteProduct(productId) {
    if (!confirm(`¿Estás seguro de eliminar el producto #${productId}?`)) return;

    try {
        const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
            method: "DELETE"
        });

        if (response.ok) {
            showNotification("Producto eliminado del sistema.", "success");
            loadProducts();
        } else {
            showNotification("No se pudo eliminar el producto especificado.", "error");
        }
    } catch (error) {
        console.error("Error en petición DELETE:", error);
        showNotification("Error en el servidor al intentar eliminar.", "error");
    }
}

/**
 * Módulo 4: Cargar Invoices u Órdenes (FR7 - Business Intelligence)
 */
async function loadOrders() {
    try {
        const response = await fetch(`${API_BASE_URL}/orders`);
        const data = await response.json();
        
        // Maneja la respuesta tanto si devuelve una lista ([]) o un objeto ({ orders: [] })
        const orders = Array.isArray(data) ? data : (data.orders || []);
        
        const tableBody = document.getElementById('orders-table-body');
        if (!tableBody) return;
        
        tableBody.innerHTML = '';
        
        orders.forEach(order => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>#${order.id || order.order_id || ''}</td>
                <td>${order.customer_name || order.user_id || 'Cliente'}</td>
                <td>$${parseFloat(order.total_amount || order.total || 0).toFixed(2)}</td>
                <td><span class="badge bg-success">${order.status || 'Completado'}</span></td>
            `;
            tableBody.appendChild(row);
        });

        // Actualizar el contador de órdenes si existe
        const ordersCount = document.getElementById('orders-count');
        if (ordersCount) {
            ordersCount.textContent = orders.length;
        }

    } catch (error) {
        console.error('Error al cargar órdenes:', error);
        showNotification("Error al cargar la lista de órdenes.", "error");
    }
}

/**
 * Componente UI: Feedback visual de notificaciones
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