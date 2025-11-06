// Main JavaScript for Admin Dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

function initializeDashboard() {
    setupMobileMenu();
    setupDropdowns();
    setupToasts();
    setupAnimations();
}

// Mobile Menu Toggle
function setupMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if (mobileMenuBtn && sidebar && overlay) {
        mobileMenuBtn.addEventListener('click', () => {
            sidebar.classList.toggle('translate-x-full');
            overlay.classList.toggle('hidden');
        });

        overlay.addEventListener('click', () => {
            sidebar.classList.add('translate-x-full');
            overlay.classList.add('hidden');
        });
    }
}

// Profile Dropdown
function setupDropdowns() {
    const profileDropdownBtn = document.getElementById('profile-dropdown-btn');
    const profileDropdown = document.getElementById('profile-dropdown');

    if (profileDropdownBtn && profileDropdown) {
        profileDropdownBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            profileDropdown.classList.toggle('hidden');
        });

        document.addEventListener('click', () => {
            profileDropdown.classList.add('hidden');
        });

        profileDropdown.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }
}

// Toast Notifications
function setupToasts() {
    window.showToast = function(message, type = 'info', duration = 3000) {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast-notification transform translate-x-full transition-transform duration-300 ease-in-out p-4 rounded-lg shadow-lg max-w-sm ${getToastClasses(type)}`;
        
        toast.innerHTML = `
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    ${getToastIcon(type)}
                </div>
                <div class="mr-3">
                    <p class="text-sm font-medium">${message}</p>
                </div>
                <div class="mr-auto pl-3">
                    <div class="-mx-1.5 -my-1.5">
                        <button onclick="closeToast(this)" class="inline-flex p-1.5 rounded-md hover:bg-opacity-75 focus:outline-none">
                            <i class="fas fa-times text-sm"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;

        container.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.remove('translate-x-full');
        }, 100);

        setTimeout(() => {
            closeToast(toast.querySelector('button'));
        }, duration);
    };
}

function getToastClasses(type) {
    switch (type) {
        case 'success':
            return 'bg-green-500 text-white';
        case 'error':
            return 'bg-red-500 text-white';
        case 'warning':
            return 'bg-yellow-500 text-white';
        default:
            return 'bg-blue-500 text-white';
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
    const toast = button.closest('.toast-notification');
    if (toast) {
        toast.classList.add('translate-x-full');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }
}

// Animations
function setupAnimations() {
    const cards = document.querySelectorAll('.hover\\:shadow-lg');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('ar-EG', {
        style: 'currency',
        currency: 'EGP'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('ar-EG', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

// API Helper
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showToast('حدث خطأ في الاتصال بالخادم', 'error');
        throw error;
    }
}
