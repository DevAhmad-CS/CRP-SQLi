/**
 * Card 3D Tilt Effect
 * Cards tilt in 3D space when hovering, following mouse movement
 * Creates a professional interactive effect
 */

document.addEventListener('DOMContentLoaded', function() {
    initCard3DTilt();
});

/**
 * Initialize 3D tilt effect for cards
 */
function initCard3DTilt() {
    const cards = document.querySelectorAll('.stat-card, .example-card');
    
    cards.forEach(card => {
        let isHovering = false;
        let currentRotateX = 0;
        let currentRotateY = 0;
        let targetRotateX = 0;
        let targetRotateY = 0;
        
        // Tilt intensity (how much the card tilts)
        const maxTilt = 15; // degrees
        const perspective = 1000; // CSS perspective value
        
        // Set perspective on card container
        const cardStyle = window.getComputedStyle(card);
        if (!card.parentElement.style.perspective) {
            card.parentElement.style.perspective = `${perspective}px`;
            card.parentElement.style.perspectiveOrigin = 'center center';
        }
        
        // Smooth animation using requestAnimationFrame
        function animate() {
            if (isHovering) {
                // Smooth interpolation
                currentRotateX += (targetRotateX - currentRotateX) * 0.15;
                currentRotateY += (targetRotateY - currentRotateY) * 0.15;
                
                // Apply transform with 3D effect
                card.style.transform = `
                    perspective(${perspective}px)
                    rotateX(${currentRotateX}deg)
                    rotateY(${currentRotateY}deg)
                    scale3d(1.02, 1.02, 1.02)
                `;
                
                // Add shadow based on tilt
                const shadowX = currentRotateY * 2;
                const shadowY = currentRotateX * 2;
                card.style.boxShadow = `
                    ${shadowX}px ${shadowY}px 30px rgba(0, 0, 0, 0.3),
                    0 0 20px rgba(157, 122, 255, 0.2)
                `;
                
                requestAnimationFrame(animate);
            } else {
                // Return to original position
                currentRotateX += (0 - currentRotateX) * 0.15;
                currentRotateY += (0 - currentRotateY) * 0.15;
                
                if (Math.abs(currentRotateX) > 0.1 || Math.abs(currentRotateY) > 0.1) {
                    card.style.transform = `
                        perspective(${perspective}px)
                        rotateX(${currentRotateX}deg)
                        rotateY(${currentRotateY}deg)
                        scale3d(1, 1, 1)
                    `;
                    requestAnimationFrame(animate);
                } else {
                    card.style.transform = '';
                    card.style.boxShadow = '';
                }
            }
        }
        
        // Mouse enter
        card.addEventListener('mouseenter', function(e) {
            isHovering = true;
            card.style.transition = 'none'; // Disable CSS transitions during animation
            animate();
        });
        
        // Mouse move
        card.addEventListener('mousemove', function(e) {
            if (!isHovering) return;
            
            const rect = card.getBoundingClientRect();
            const cardCenterX = rect.left + rect.width / 2;
            const cardCenterY = rect.top + rect.height / 2;
            
            // Calculate mouse position relative to card center
            const mouseX = e.clientX - cardCenterX;
            const mouseY = e.clientY - cardCenterY;
            
            // Calculate tilt based on mouse position
            // Normalize to -1 to 1 range
            const normalizedX = mouseX / (rect.width / 2);
            const normalizedY = mouseY / (rect.height / 2);
            
            // Apply tilt (invert Y for natural feel)
            targetRotateY = normalizedX * maxTilt;
            targetRotateX = -normalizedY * maxTilt;
        });
        
        // Mouse leave
        card.addEventListener('mouseleave', function(e) {
            isHovering = false;
            targetRotateX = 0;
            targetRotateY = 0;
            card.style.transition = 'transform 0.5s ease-out, box-shadow 0.5s ease-out';
        });
        
        // Ensure card has proper 3D rendering
        card.style.transformStyle = 'preserve-3d';
        card.style.willChange = 'transform';
    });
}

