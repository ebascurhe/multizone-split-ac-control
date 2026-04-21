// Clima Sidebar Navigation Script

/**
 * Initialize the Clima sidebar navigation
 * Call this function when the page loads
 */
function initClimaNavigation() {
    const navLinks = document.querySelectorAll('.clima-nav-link');

    // Set active link based on current page
    const currentPage = getCurrentPageName();
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('data-page');
        if (linkPage === currentPage) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Add click handlers to navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const page = link.getAttribute('data-page');
            if (page && page !== 'current') {
                navigateToPage(page);
            }
        });
    });
}

/**
 * Get the current page name from the URL
 */
function getCurrentPageName() {
    const href = window.location.href;
    const filename = href.substring(href.lastIndexOf('/') + 1).replace('.html', '');
    return filename || 'index';
}

/**
 * Navigate to a different dashboard page
 */
function navigateToPage(page) {
    const pages = {
        'index': 'index.html',
        'calibration': 'calibration_dashboard.html',
        'overview': 'dashboard_preview.html',
        'heating': 'dashboard_heating.html',
        'schedules': 'schedules.html',
        'energy': 'energy_analytics.html'
    };

    if (pages[page]) {
        window.location.href = pages[page];
    }
}

/**
 * Update the active nav link
 */
function setActiveNavLink(pageName) {
    const navLinks = document.querySelectorAll('.clima-nav-link');
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('data-page');
        if (linkPage === pageName) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initClimaNavigation);
