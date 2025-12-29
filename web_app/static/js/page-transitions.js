/**
 * Smooth Page Transitions
 * Smooth fade out/in transitions when navigating between pages
 * Creates professional page transition experience
 */

document.addEventListener('DOMContentLoaded', function() {
    initPageTransitions();
});

/**
 * Initialize page transitions
 */
function initPageTransitions() {
    // Get all navigation links
    const navLinks = document.querySelectorAll('a[href^="/"]:not([href^="//"]):not([href^="http"])');
    
    navLinks.forEach(link => {
        // Skip if link is to current page or external
        if (link.getAttribute('href') === window.location.pathname) return;
        if (link.getAttribute('target') === '_blank') return;
        
        link.addEventListener('click', function(e) {
            // Only handle internal links
            const href = this.getAttribute('href');
            if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;
            
            // Check if it's an internal link
            if (href.startsWith('/') || href.startsWith('./') || href.startsWith('../')) {
                e.preventDefault();
                
                const targetUrl = this.getAttribute('href');
                
                // Fade out current page
                fadeOutPage(targetUrl);
            }
        });
    });
}

/**
 * Fade out current page
 * @param {string} targetUrl - URL to navigate to
 */
function fadeOutPage(targetUrl) {
    const body = document.body;
    
    // Add fade-out class
    body.style.transition = 'opacity 0.3s ease-out';
    body.style.opacity = '0';
    
    // Navigate after fade out
    setTimeout(() => {
        window.location.href = targetUrl;
    }, 300);
}

/**
 * Fade in page on load
 */
function fadeInPage() {
    const body = document.body;
    
    // Set initial state
    body.style.opacity = '0';
    body.style.transition = 'opacity 0.4s ease-in';
    
    // Fade in after a tiny delay
    requestAnimationFrame(() => {
        body.style.opacity = '1';
    });
}

// Fade in page when loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fadeInPage);
} else {
    fadeInPage();
}

