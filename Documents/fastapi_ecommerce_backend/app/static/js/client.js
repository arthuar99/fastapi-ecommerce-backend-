// Client-side JavaScript for ecommerce

document.addEventListener('DOMContentLoaded', function() {
    initializeClientApp();
});

function initializeClientApp() {
    setupMobileMenu();
    setupUserMenu();
    setupCartSidebar();
    setupSearch();
    loadCartFromStorage();
}

// Mobile Menu
function setupMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

// User Menu
function setupUserMenu() {
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userMenu = document.getElementById('userMenu');

    if (userMenuBtn && userMenu) {
        userMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            userMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', () => {
            userMenu.classList.add('hidden');
        });

        userMenu.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }
}

// Cart Sidebar
function setupCartSidebar() {
    const cartBtn = document.getElementById('cartBtn');
    const cartSidebar = document.getElementById('cartSidebar');
    const cartOverlay = document.getElementById('cartOverlay');
    const closeCartBtn = document.getElementById('closeCartBtn');

    if (cartBtn && cartSidebar) {
        cartBtn.addEventListener('click', openCart);
    }

    if (closeCartBtn) {
        closeCartBtn.addEventListener('click', closeCart);
    }

    if (cartOverlay) {
        cartOverlay.addEventListener('click', closeCart);
    }
}

function openCart() {
    const cartSidebar = document.getElementById('cartSidebar');
    const cartOverlay = document.getElementById('cartOverlay');
    
    cartSidebar.classList.remove('-translate-x-full');
    cartOverlay.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeCart() {
    const cartSidebar = document.getElementById('cartSidebar');
    const cartOverlay = document.getElementById('cartOverlay');
    
    cartSidebar.classList.add('-translate-x-full');
    cartOverlay.classList.add('hidden');
    document.body.style.overflow = 'auto';
}

// Search functionality
function setupSearch() {
    const searchInputs = document.querySelectorAll('#searchInput, input[placeholder*="ابحث"]');
    
    searchInputs.forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch(input.value);
            }
        });
    });

    // Search button click handlers
    const searchBtns = document.querySelectorAll('button:has(.fa-search)');
    searchBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const input = btn.parentElement.querySelector('input') || 
                         btn.parentElement.parentElement.querySelector('input');
            if (input) {
                performSearch(input.value);
            }
        });
    });
}

function performSearch(query) {
    if (query.trim()) {
        window.location.href = `/products?search=${encodeURIComponent(query)}`;
    }
}

// Cart Management
let cart = [];

function loadCartFromStorage() {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
        updateCartUI();
    }
}

function saveCartToStorage() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function addToCart(productId, productName = 'منتج', productPrice = 0, productImage = '') {
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: productId,
            name: productName,
            price: productPrice,
            image: productImage,
            quantity: 1
        });
    }
    
    saveCartToStorage();
    updateCartUI();
    showCartAnimation();
    showToast('تم إضافة المنتج إلى السلة!', 'success');
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    saveCartToStorage();
    updateCartUI();
    showToast('تم حذف المنتج من السلة', 'info');
}

function updateCartQuantity(productId, quantity) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        if (quantity <= 0) {
            removeFromCart(productId);
        } else {
            item.quantity = quantity;
            saveCartToStorage();
            updateCartUI();
        }
    }
}

function updateCartUI() {
    const cartCount = document.getElementById('cartCount');
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');
    
    // Update cart count
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    if (cartCount) {
        cartCount.textContent = totalItems;
        cartCount.style.display = totalItems > 0 ? 'flex' : 'none';
    }
    
    // Update cart total
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    if (cartTotal) {
        cartTotal.textContent = `${total.toFixed(2)} ج.م`;
    }
    
    // Update cart items
    if (cartItems) {
        if (cart.length === 0) {
            cartItems.innerHTML = `
                <div class="text-center py-12 text-gray-500">
                    <i class="fas fa-shopping-cart text-4xl mb-4"></i>
                    <p>السلة فارغة</p>
                </div>
            `;
        } else {
            cartItems.innerHTML = cart.map(item => `
                <div class="flex items-center space-x-4 space-x-reverse p-4 border-b">
                    <img src="${item.image || '/static/images/placeholder.jpg'}" alt="${item.name}" class="w-16 h-16 object-cover rounded-lg">
                    <div class="flex-1">
                        <h4 class="font-medium text-sm">${item.name}</h4>
                        <p class="text-primary-600 font-bold">${item.price} ج.م</p>
                        <div class="flex items-center space-x-2 space-x-reverse mt-2">
                            <button onclick="updateCartQuantity(${item.id}, ${item.quantity - 1})" class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center hover:bg-gray-300">
                                <i class="fas fa-minus text-xs"></i>
                            </button>
                            <span class="mx-2 font-medium">${item.quantity}</span>
                            <button onclick="updateCartQuantity(${item.id}, ${item.quantity + 1})" class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center hover:bg-gray-300">
                                <i class="fas fa-plus text-xs"></i>
                            </button>
                        </div>
                    </div>
                    <button onclick="removeFromCart(${item.id})" class="text-red-500 hover:text-red-700">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `).join('');
        }
    }
}

function showCartAnimation() {
    const cartBtn = document.getElementById('cartBtn');
    if (cartBtn) {
        cartBtn.classList.add('animate-bounce');
        setTimeout(() => {
            cartBtn.classList.remove('animate-bounce');
        }, 1000);
    }
}

// Toast Notifications
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 z-50 p-4 rounded-lg text-white transform translate-x-full transition-transform duration-300 ${getToastClasses(type)}`;
    
    toast.innerHTML = `
        <div class="flex items-center">
            <div class="flex-shrink-0">
                ${getToastIcon(type)}
            </div>
            <div class="mr-3">
                <p class="text-sm font-medium">${message}</p>
            </div>
            <div class="mr-auto pl-3">
                <button onclick="closeToast(this)" class="text-white hover:text-gray-200">
                    <i class="fas fa-times text-sm"></i>
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.remove('translate-x-full');
    }, 100);
    
    setTimeout(() => {
        closeToast(toast.querySelector('button'));
    }, duration);
}

function getToastClasses(type) {
    switch (type) {
        case 'success':
            return 'bg-green-500';
        case 'error':
            return 'bg-red-500';
        case 'warning':
            return 'bg-yellow-500';
        default:
            return 'bg-blue-500';
    }
}

function getToastIcon(type) {
    switch (type) {
        case 'success':
            return '<i class="fas fa-check-circle text-white"></i>';
        case 'error':
            return '<i class="fas fa-exclamation-circle text-white"></i>';
        case 'warning':
            return '<i class="fas fa-exclamation-triangle text-white"></i>';
        default:
            return '<i class="fas fa-info-circle text-white"></i>';
    }
}

function closeToast(button) {
    const toast = button.closest('.fixed');
    if (toast) {
        toast.classList.add('translate-x-full');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }
}

// Utility Functions
function formatCurrency(amount) {
    return `${parseFloat(amount).toFixed(2)} ج.م`;
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Product interactions
function quickView(productId) {
    console.log('Quick view for product:', productId);
    // Implementation for quick view modal
    showToast('جارٍ تحميل المنتج...', 'info');
}

function addToWishlist(productId) {
    console.log('Add to wishlist:', productId);
    showToast('تم إضافة المنتج إلى قائمة الأمنيات!', 'success');
}

// Initialize cart on page load
window.addEventListener('load', () => {
    loadCartFromStorage();
});
