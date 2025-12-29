/**
 * Button Click Particles Effect
 * Creates particle effect when buttons are clicked
 * Adds micro-interaction feedback
 */

document.addEventListener('DOMContentLoaded', function() {
    initButtonParticles();
});

/**
 * Initialize particle effect for buttons
 */
function initButtonParticles() {
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-example');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            createParticles(e, button);
        });
    });
}

/**
 * Create particles at click position
 * @param {MouseEvent} e - Click event
 * @param {HTMLElement} button - Button element
 */
function createParticles(e, button) {
    const rect = button.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    // Get button color from computed style
    const computedStyle = window.getComputedStyle(button);
    const bgColor = computedStyle.background || computedStyle.backgroundColor || '#9d7aff';
    
    // Extract color from gradient or solid color
    let particleColor = '#9d7aff'; // Default purple
    if (bgColor.includes('rgb')) {
        particleColor = bgColor.match(/rgb\([^)]+\)/)?.[0] || particleColor;
    } else if (bgColor.includes('#')) {
        particleColor = bgColor.match(/#[0-9a-fA-F]{6}/)?.[0] || particleColor;
    }
    
    // Create 8-12 particles
    const particleCount = 8 + Math.floor(Math.random() * 5);
    
    for (let i = 0; i < particleCount; i++) {
        createParticle(x, y, particleColor, button);
    }
}

/**
 * Create a single particle
 * @param {number} x - X position relative to button
 * @param {number} y - Y position relative to button
 * @param {string} color - Particle color
 * @param {HTMLElement} button - Button element
 */
function createParticle(x, y, color, button) {
    const particle = document.createElement('div');
    
    // Random size (2-4px)
    const size = 2 + Math.random() * 2;
    
    // Random direction and speed
    const angle = (Math.PI * 2 * Math.random());
    const velocity = 30 + Math.random() * 40;
    const vx = Math.cos(angle) * velocity;
    const vy = Math.sin(angle) * velocity;
    
    // Random lifetime (300-600ms)
    const lifetime = 300 + Math.random() * 300;
    
    // Style particle
    particle.style.cssText = `
        position: absolute;
        left: ${x}px;
        top: ${y}px;
        width: ${size}px;
        height: ${size}px;
        background: ${color};
        border-radius: 50%;
        pointer-events: none;
        z-index: 1000;
        opacity: 1;
        box-shadow: 0 0 ${size * 2}px ${color};
    `;
    
    // Append to button (button must have position: relative)
    if (window.getComputedStyle(button).position === 'static') {
        button.style.position = 'relative';
    }
    button.appendChild(particle);
    
    // Animate particle
    const startTime = performance.now();
    
    function animate(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = elapsed / lifetime;
        
        if (progress >= 1) {
            particle.remove();
            return;
        }
        
        // Calculate position with gravity
        const currentX = x + vx * progress;
        const currentY = y + vy * progress + (progress * progress * 100); // Gravity effect
        
        // Fade out
        const opacity = 1 - progress;
        const scale = 1 - progress * 0.5;
        
        particle.style.transform = `translate(${currentX - x}px, ${currentY - y}px) scale(${scale})`;
        particle.style.opacity = opacity;
        
        requestAnimationFrame(animate);
    }
    
    requestAnimationFrame(animate);
}

