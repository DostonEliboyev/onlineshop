// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Show toast notification
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toastId = 'toast-' + Date.now();
    const bgClass = type === 'success' ? 'bg-dark' : type === 'error' ? 'bg-danger' : 'bg-info';

    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'x-circle' : 'info-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', toastHTML);
    const toastEl = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();

    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

// Update cart badge in navbar
function updateCartBadge(count) {
    const badge = document.getElementById('cart-badge');
    if (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline' : 'none';
    }
}

// Add to Cart (AJAX)
function addToCart(productId, quantity) {
    quantity = quantity || 1;

    const formData = new FormData();
    formData.append('quantity', quantity);

    fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showToast(data.message, 'success');
            updateCartBadge(data.cart_count);
        } else {
            showToast(data.message || 'Error adding to cart', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error adding to cart', 'error');
    });
}

// Toggle Favorite (AJAX)
function toggleFavorite(productId, btn) {
    fetch(`/favorites/toggle/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        const icon = btn.querySelector('i');
        if (data.status === 'added') {
            icon.className = 'bi bi-heart-fill text-danger';
            if (btn.id === 'detail-fav-btn') {
                btn.className = 'btn btn-danger mb-4';
                btn.innerHTML = '<i class="bi bi-heart-fill me-1"></i> Remove from Favorites';
            }
            showToast(data.message, 'success');
        } else if (data.status === 'removed') {
            icon.className = 'bi bi-heart';
            if (btn.id === 'detail-fav-btn') {
                btn.className = 'btn btn-outline-danger mb-4';
                btn.innerHTML = '<i class="bi bi-heart me-1"></i> Add to Favorites';
            }
            showToast(data.message, 'info');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Please log in to add favorites', 'error');
    });
}

// Initialize product card swipers
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[class*="product-swiper-"]').forEach(el => {
        new Swiper(el, {
            loop: true,
            autoplay: { delay: 4000, disableOnInteraction: true },
            pagination: {
                el: el.querySelector('.swiper-pagination'),
                clickable: true,
            },
        });
    });
});
