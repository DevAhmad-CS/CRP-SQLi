/**
 * Number Counter Animation
 * Animates numbers from 0 to target value
 * Used in statistics page for stat-value elements
 */

document.addEventListener('DOMContentLoaded', function() {
    initNumberCounters();
});

/**
 * Initialize number counter animation for elements with stat-value class
 */
function initNumberCounters() {
    const counterElements = document.querySelectorAll('.stat-value');
    
    // Create Intersection Observer to trigger animation when element enters viewport
    const observerOptions = {
        threshold: 0.5, // Trigger when 50% of element is visible
        rootMargin: '0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                // Only animate if not already animated
                if (!element.dataset.animated) {
                    animateCounter(element);
                    element.dataset.animated = 'true';
                    // Unobserve after animation starts
                    observer.unobserve(element);
                }
            }
        });
    }, observerOptions);
    
    // Observe all counter elements
    counterElements.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Animate counter from 0 to target value
 * @param {HTMLElement} element - The element containing the number
 */
function animateCounter(element) {
    const text = element.textContent.trim();
    
    // Extract number and unit (e.g., "99.53%" -> number: 99.53, unit: "%")
    const match = text.match(/(\d+\.?\d*)(.*)/);
    if (!match) return;
    
    const targetValue = parseFloat(match[1]);
    const unit = match[2] || ''; // "%", " samples", etc.
    
    if (isNaN(targetValue)) return;
    
    // Animation settings
    const duration = 2000; // 2 seconds
    const startTime = performance.now();
    const startValue = 0;
    
    // Easing function (ease-out cubic)
    function easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }
    
    // Animation function
    function animate(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Apply easing
        const easedProgress = easeOutCubic(progress);
        
        // Calculate current value
        const currentValue = startValue + (targetValue - startValue) * easedProgress;
        
        // Format number based on original format
        let formattedValue;
        if (text.includes('.')) {
            // Decimal number (e.g., 99.53)
            formattedValue = currentValue.toFixed(2);
        } else {
            // Integer (e.g., 17794)
            formattedValue = Math.floor(currentValue).toString();
        }
        
        // Update element text
        element.textContent = formattedValue + unit;
        
        // Continue animation if not finished
        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            // Ensure final value is exact
            element.textContent = text;
        }
    }
    
    // Start animation
    requestAnimationFrame(animate);
}

