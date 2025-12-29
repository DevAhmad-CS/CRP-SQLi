/**
 * Navbar Scroll Hide/Show
 * Navbar hides when scrolling down and shows when scrolling up
 * Creates a clean, modern navigation experience
 */

document.addEventListener('DOMContentLoaded', function() {
    initNavbarScroll();
});

/**
 * Initialize navbar scroll behavior
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    let lastScrollY = window.scrollY || window.pageYOffset;
    let isScrollingDown = false;
    let ticking = false;
    
    // Scroll threshold (hide navbar only after scrolling this much)
    const scrollThreshold = 50; // pixels
    
    function updateNavbar() {
        const currentScrollY = window.scrollY || window.pageYOffset;
        const scrollDelta = currentScrollY - lastScrollY;
        
        // Determine scroll direction
        isScrollingDown = scrollDelta > 0;
        
        // Only hide/show if scrolled past threshold
        if (Math.abs(scrollDelta) > 5) { // Minimum scroll to trigger
            if (currentScrollY > scrollThreshold) {
                if (isScrollingDown) {
                    // Scrolling down - hide navbar
                    navbar.style.transform = 'translateY(-100%)';
                    navbar.style.opacity = '0';
                } else {
                    // Scrolling up - show navbar
                    navbar.style.transform = 'translateY(0)';
                    navbar.style.opacity = '1';
                }
            } else {
                // At top of page - always show
                navbar.style.transform = 'translateY(0)';
                navbar.style.opacity = '1';
            }
        }
        
        lastScrollY = currentScrollY;
        ticking = false;
    }
    
    // Ensure navbar has transition
    navbar.style.transition = 'transform 0.3s ease-out, opacity 0.3s ease-out';
    navbar.style.willChange = 'transform, opacity';
    
    // Throttle scroll events
    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(updateNavbar);
            ticking = true;
        }
    }, { passive: true });
    
    // Show navbar on mouse move near top
    let mouseMoveTimeout;
    window.addEventListener('mousemove', function(e) {
        // Only show if mouse is near top of page
        if (e.clientY < 100) {
            clearTimeout(mouseMoveTimeout);
            navbar.style.transform = 'translateY(0)';
            navbar.style.opacity = '1';
            
            // Hide again after mouse leaves top area
            mouseMoveTimeout = setTimeout(function() {
                if (window.scrollY > scrollThreshold && isScrollingDown) {
                    navbar.style.transform = 'translateY(-100%)';
                    navbar.style.opacity = '0';
                }
            }, 2000);
        }
    }, { passive: true });
}

