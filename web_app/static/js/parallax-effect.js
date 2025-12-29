/**
 * Parallax Effect (Light)
 * Subtle parallax effect on elements when scrolling
 * Creates depth and visual interest without being overwhelming
 */

document.addEventListener('DOMContentLoaded', function() {
    initParallaxEffect();
});

/**
 * Initialize parallax effect
 */
function initParallaxEffect() {
    // Elements to apply parallax effect
    const parallaxElements = document.querySelectorAll('.page-hero, .hero-section');
    
    if (parallaxElements.length === 0) return;
    
    let ticking = false;
    
    function updateParallax() {
        const scrollY = window.scrollY || window.pageYOffset;
        
        parallaxElements.forEach(element => {
            // Get element position
            const rect = element.getBoundingClientRect();
            const elementTop = rect.top + scrollY;
            const elementHeight = rect.height;
            
            // Calculate if element is in viewport
            const viewportTop = scrollY;
            const viewportBottom = scrollY + window.innerHeight;
            
            if (elementTop + elementHeight > viewportTop && elementTop < viewportBottom) {
                // Calculate parallax offset (subtle effect)
                const parallaxSpeed = 0.3; // 30% of scroll speed (light effect)
                const elementCenter = elementTop + elementHeight / 2;
                const viewportCenter = viewportTop + window.innerHeight / 2;
                const distanceFromCenter = viewportCenter - elementCenter;
                
                // Apply parallax transform
                const parallaxOffset = distanceFromCenter * parallaxSpeed;
                
                // Apply transform with will-change for performance
                element.style.transform = `translateY(${parallaxOffset}px)`;
                element.style.willChange = 'transform';
            }
        });
        
        ticking = false;
    }
    
    // Throttle scroll events for better performance
    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    }, { passive: true });
    
    // Initial update
    updateParallax();
    
    // Update on window resize
    window.addEventListener('resize', function() {
        updateParallax();
    }, { passive: true });
}

