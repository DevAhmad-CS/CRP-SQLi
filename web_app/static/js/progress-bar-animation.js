/**
 * Progress Bar Animation
 * Animates progress bars from 0% to target value
 * Used for confidence bars in results
 */

/**
 * Animate progress bar from 0 to target value
 * @param {HTMLElement} progressBar - The progress bar element
 * @param {number} targetValue - Target percentage (0-100)
 * @param {number} duration - Animation duration in milliseconds
 */
function animateProgressBar(progressBar, targetValue, duration = 1000) {
    if (!progressBar) return;
    
    // Reset to 0
    progressBar.style.width = '0%';
    
    // Animation settings
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
        
        // Update progress bar width
        progressBar.style.width = currentValue + '%';
        
        // Update text if exists
        const textElement = progressBar.querySelector('span, div');
        if (textElement && textElement.textContent) {
            textElement.textContent = Math.round(currentValue) + '%';
        }
        
        // Continue animation if not finished
        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            // Ensure final value is exact
            progressBar.style.width = targetValue + '%';
            if (textElement) {
                textElement.textContent = Math.round(targetValue) + '%';
            }
        }
    }
    
    // Start animation after a small delay for better visual effect
    setTimeout(() => {
        requestAnimationFrame(animate);
    }, 100);
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = animateProgressBar;
}

