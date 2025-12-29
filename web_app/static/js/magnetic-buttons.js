/**
 * Magnetic Buttons Effect
 * Buttons follow mouse cursor slightly when hovering
 * Creates a magnetic attraction effect
 */

document.addEventListener('DOMContentLoaded', function() {
    initMagneticButtons();
});

/**
 * Initialize magnetic effect for buttons
 */
function initMagneticButtons() {
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-example');
    
    buttons.forEach(button => {
        // Skip if button is disabled
        if (button.disabled) return;
        
        let isHovering = false;
        let currentX = 0;
        let currentY = 0;
        let targetX = 0;
        let targetY = 0;
        
        // Magnetic strength (how much the button moves)
        const strength = 0.3; // 30% of mouse distance
        
        // Smooth animation using requestAnimationFrame
        function animate() {
            if (isHovering) {
                // Smooth interpolation
                currentX += (targetX - currentX) * 0.1;
                currentY += (targetY - currentY) * 0.1;
                
                // Apply transform - preserve existing CSS transforms (scale, translateY from hover)
                const existingTransform = button.dataset.originalTransform || '';
                button.style.transform = `${existingTransform} translate(${currentX}px, ${currentY}px)`;
                
                requestAnimationFrame(animate);
            } else {
                // Return to original position
                currentX += (0 - currentX) * 0.1;
                currentY += (0 - currentY) * 0.1;
                
                if (Math.abs(currentX) > 0.01 || Math.abs(currentY) > 0.01) {
                    const existingTransform = button.dataset.originalTransform || '';
                    button.style.transform = `${existingTransform} translate(${currentX}px, ${currentY}px)`;
                    requestAnimationFrame(animate);
                } else {
                    // Restore original transform or clear if none
                    button.style.transform = button.dataset.originalTransform || '';
                }
            }
        }
        
        // Store original transform from CSS
        const computedStyle = window.getComputedStyle(button);
        const originalTransform = computedStyle.transform;
        if (originalTransform && originalTransform !== 'none') {
            button.dataset.originalTransform = originalTransform;
        } else {
            button.dataset.originalTransform = '';
        }
        
        // Mouse enter
        button.addEventListener('mouseenter', function(e) {
            isHovering = true;
            animate();
        });
        
        // Mouse move
        button.addEventListener('mousemove', function(e) {
            if (!isHovering) return;
            
            const rect = button.getBoundingClientRect();
            const buttonCenterX = rect.left + rect.width / 2;
            const buttonCenterY = rect.top + rect.height / 2;
            
            // Calculate distance from center
            const deltaX = (e.clientX - buttonCenterX) * strength;
            const deltaY = (e.clientY - buttonCenterY) * strength;
            
            // Limit maximum movement (prevent button from moving too far)
            const maxDistance = 15; // pixels
            const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            
            if (distance > maxDistance) {
                targetX = (deltaX / distance) * maxDistance;
                targetY = (deltaY / distance) * maxDistance;
            } else {
                targetX = deltaX;
                targetY = deltaY;
            }
        });
        
        // Mouse leave
        button.addEventListener('mouseleave', function(e) {
            isHovering = false;
            targetX = 0;
            targetY = 0;
        });
        
        // Preserve existing hover styles by wrapping them
        const originalHover = button.style.transform || '';
    });
}

