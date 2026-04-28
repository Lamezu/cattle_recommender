document.addEventListener('DOMContentLoaded', () => {
    checkSession();
});

async function checkSession() {
    const response = await fetch('/api/current_user');
    if (response.ok) {
        const user = await response.json();
        const firstName = user.name.split(' ')[0];
        document.getElementById('current-farmer-name').innerText = `Hola, ${firstName}`;
        // Ponemos la inicial dinámica en el avatar
        document.querySelector('.avatar').innerText = firstName.charAt(0).toUpperCase();
        
        document.body.setAttribute('data-user-id', user.id);
        switchTab('recommended');
    } else {
        window.location.href = '/login';
    }
}

function loadFarmerData() {
    const farmerId = document.getElementById('farmer-select').value;
    if (!farmerId) return;

    const farmerName = document.getElementById('farmer-select').options[document.getElementById('farmer-select').selectedIndex].text;
    document.getElementById('current-farmer-name').innerText = `Hola, ${farmerName.split(' ')[0]}`;
    
    switchTab('recommended');
}

let currentPage = 1;
let currentTab = 'recommended';
const itemsPerPage = 15;

async function switchTab(tab, element = null, page = 1) {
    currentPage = page;
    currentTab = tab;
    const farmerId = document.body.getAttribute('data-user-id');
    const grid = document.getElementById('cows-grid');
    
    const targetElement = element || document.querySelector(`.tab-btn[onclick*="'${tab}'"]`) || document.querySelector(`.nav-item[onclick*="'${tab}'"]`);

    // SI EL USUARIO HA HECHO CLIC (element != null), RESETEAMOS FILTROS
    if (element) {
        document.getElementById('breed-filter').value = 'Todas';
        document.getElementById('main-search').value = '';
        document.getElementById('sort-filter').value = 'id_asc';
    }

    let loadingMsg = "Buscando las mejores opciones...";
    if (tab === 'purchases') loadingMsg = "Consultando tu historial de compras...";
    if (tab === 'catalog') loadingMsg = "Abriendo el catálogo completo...";
    
    grid.innerHTML = `<div class="loader">${loadingMsg}</div>`;

    const heroTitle = document.querySelector('.hero-section h1');
    const heroDesc = document.querySelector('.hero-section p');
    const tabsSection = document.querySelector('.tabs-header');

    try {
        let url = '';
        const breed = document.getElementById('breed-filter').value;
        const search = document.getElementById('main-search').value;
        const sort = document.getElementById('sort-filter').value;

        const filterParams = `?breed=${breed}&search=${search}&sort=${sort}`;

        switch(tab) {
            case 'recommended': url = `/api/recommendations/${farmerId}${filterParams}`; break;
            case 'catalog': url = `/api/catalog${filterParams}&page=${page}&limit=${itemsPerPage}`; break;
            case 'top-rated': url = `/api/top-rated${filterParams}`; break;
            case 'most-purchased': url = `/api/most-purchased${filterParams}`; break;
            case 'purchases': url = `/api/purchases/${farmerId}${filterParams}`; break;
        }

        const response = await fetch(url);
        if (!response.ok) throw new Error("Error en la respuesta del servidor");
        
        const data = await response.json();
        const cows = Array.isArray(data) ? data : data.cows;
        const total = data.total || 0;
        
        if (tab === 'purchases' && cows.length === 0) {
            showNotification("Sin Compras", "Todavía no has realizado ninguna compra. ¡Explora el catálogo!", "error");
            switchTab('catalog');
            return;
        }

        // ÉXITO: Marcamos activo y actualizamos textos
        document.querySelectorAll('.tab-btn, .nav-item').forEach(el => el.classList.remove('active'));
        if (targetElement) targetElement.classList.add('active');

        // Actualizamos textos del héroe
        if (tab === 'purchases') {
            heroTitle.innerText = "Mi Historial de Compras";
            heroDesc.innerText = "Gestiona tus adquisiciones y devoluciones de forma directa.";
            tabsSection.style.display = 'none';
        } else {
            heroTitle.innerText = "Descubre las mejores opciones para tu ganadería";
            heroDesc.innerText = "Algoritmos de recomendación basados en grafos y preferencias reales.";
            tabsSection.style.display = 'flex';
        }
        
        // Barra de filtros siempre disponible para búsqueda inteligente global
        document.getElementById('advanced-filters-bar').style.display = 'flex';

        renderCows(cows, grid, tab);

        // Renderizar paginación solo en catálogo
        const paginationContainer = document.getElementById('pagination-container');
        if (tab === 'catalog') {
            renderPagination(total, page);
            paginationContainer.style.display = 'flex';
        } else {
            paginationContainer.style.display = 'none';
        }
    } catch (error) {
        grid.innerHTML = `<div class="error-msg">Vaya, algo ha fallado: ${error.message}</div>`;
    }
}

function renderCows(cows, container, context = 'catalog') {
    container.innerHTML = '';
    if (cows.length === 0) {
        container.innerHTML = '<p class="empty-msg">No se han encontrado opciones en este momento.</p>';
        return;
    }

    cows.forEach(cow => {
        const breedImg = cow.breed.toLowerCase().replace(/\s+/g, '') + '.jpg';
        const card = document.createElement('div');
        card.className = 'cow-card';
        
        // Lógica de resaltado
        const searchTerm = document.getElementById('main-search').value;
        let displayName = cow.name;
        if (searchTerm && searchTerm.length > 0) {
            const regex = new RegExp(`(${searchTerm})`, 'gi');
            displayName = displayName.replace(regex, '<span class="highlight">$1</span>');
        }

        // Botón condicional según el contexto (CRUD)
        const actionButton = context === 'purchases' 
            ? `<button class="buy-btn" style="background: #ef4444; color: white;" onclick="returnCow('${cow.cow_id}')">Devolver</button>`
            : `<button class="buy-btn" onclick="buyCow('${cow.cow_id}')">Comprar</button>`;

        card.innerHTML = `
            <div class="cow-image-container">
                <img src="/static/img/breeds/${breedImg}" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" alt="${cow.breed}">
                <div class="cow-image-placeholder" style="display:none">
                    <i class="fas fa-cow"></i>
                </div>
            </div>
            <div class="cow-info">
                <h3>${displayName}</h3>
                <p><i class="fas fa-tag"></i> ${cow.breed} • <i class="fas fa-history"></i> ${cow.age} años</p>
                <div class="card-footer">
                    <span class="price">${cow.price}€</span>
                    ${actionButton}
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

async function loadSimilar(cowId, cowName) {
    const modal = document.getElementById('similar-modal');
    const grid = document.getElementById('similar-grid');
    document.getElementById('modal-cow-name').innerText = cowName;
    
    modal.style.display = 'block';
    grid.innerHTML = 'Cargando similares...';

    const response = await fetch(`/api/similar/${cowId}`);
    const cows = await response.json();
    renderCows(cows, grid);
}

function closeModal() {
    document.getElementById('similar-modal').style.display = 'none';
}

function openLogoutModal() {
    document.getElementById('logout-modal').style.display = 'block';
}

function closeLogoutModal() {
    document.getElementById('logout-modal').style.display = 'none';
}

async function buyCow(cowId) {
    const farmerId = document.body.getAttribute('data-user-id');
    if (!farmerId) {
        showNotification("Acceso denegado", "Por favor, inicia sesión para realizar compras.", "error");
        return;
    }

    const response = await fetch('/api/buy', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({farmer_id: farmerId, cow_id: cowId})
    });
    
    const result = await response.json();
    if (result.success) {
        showNotification("¡Éxito!", "Vaca comprada correctamente. La base de datos se ha actualizado.", "success");
        switchTab('recommended');
    }
}

async function returnCow(cowId) {
    const farmerId = document.body.getAttribute('data-user-id');
    
    const response = await fetch('/api/return', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({farmer_id: farmerId, cow_id: cowId})
    });
    
    const result = await response.json();
    if (result.success) {
        showNotification("Devolución", "La vaca ha sido devuelta y eliminada de tu historial.", "info");
        switchTab('purchases'); // Recargar la lista de compras
    }
}

function showNotification(title, message, type = 'info') {
    const container = document.getElementById('notifications-container');
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    const icon = type === 'success' ? 'fa-check-circle' : (type === 'error' ? 'fa-exclamation-triangle' : 'fa-info-circle');
    
    notification.innerHTML = `
        <i class="fas ${icon}"></i>
        <div class="notification-content">
            <b>${title}</b>
            <p>${message}</p>
        </div>
    `;
    
    container.appendChild(notification);
    
    // Animación de entrada
    setTimeout(() => notification.classList.add('show'), 10);
    
    // Eliminar automáticamente tras 5 segundos
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 500);
    }, 5000);
}

function renderPagination(total, currentPage) {
    const container = document.getElementById('pagination-container');
    const totalPages = Math.ceil(total / itemsPerPage);
    
    container.innerHTML = `
        <button class="pagination-btn" ${currentPage <= 1 ? 'disabled' : ''} onclick="switchTab('catalog', null, ${currentPage - 1})">
            <i class="fas fa-chevron-left"></i> Anterior
        </button>
        <div class="page-info">Página <span>${currentPage}</span> de ${totalPages}</div>
        <button class="pagination-btn" ${currentPage >= totalPages ? 'disabled' : ''} onclick="switchTab('catalog', null, ${currentPage + 1})">
            Siguiente <i class="fas fa-chevron-right"></i>
        </button>
    `;
}

let searchTimeout;
function applyFilters() {
    clearTimeout(searchTimeout);
    
    // Recarga la sección actual aplicando los filtros globales de forma inteligente
    searchTimeout = setTimeout(() => {
        switchTab(currentTab, null, 1);
    }, 300);
}
