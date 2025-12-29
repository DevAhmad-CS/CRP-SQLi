/**
 * Smooth Scroll Progress Indicator
 * Shows a progress bar at the top of the page indicating scroll position
 */

document.addEventListener('DOMContentLoaded', function() {
    initScrollProgress();
});

/**
 * Initialize scroll progress indicator
 */
function initScrollProgress() {
    // Create progress bar element
    const progressBar = document.createElement('div');
    progressBar.id = 'scroll-progress';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        width: 0%;
        background: linear-gradient(90deg, #9d7aff 0%, #7c5aff 100%);
        z-index: 10000;
        transition: width 0.1s ease-out;
        box-shadow: 0 0 10px rgba(157, 122, 255, 0.5);
    `;
    
    // Insert progress bar at the beginning of body
    document.body.insertBefore(progressBar, document.body.firstChild);
    
    // Update progress on scroll
    let ticking = false;
    
    function updateProgress() {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        const scrollTop = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
        
        // Calculate scroll percentage
        const scrollableHeight = documentHeight - windowHeight;
        const scrollPercentage = scrollableHeight > 0 
            ? (scrollTop / scrollableHeight) * 100 
            : 0;
        
        // Update progress bar width
        progressBar.style.width = Math.min(scrollPercentage, 100) + '%';
        
        ticking = false;
    }
    
    // Throttle scroll events for better performance
    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(updateProgress);
            ticking = true;
        }
    }, { passive: true });
    
    // Initial update
    updateProgress();
    
    // Update on window resize
    window.addEventListener('resize', function() {
        updateProgress();
    }, { passive: true });
}

