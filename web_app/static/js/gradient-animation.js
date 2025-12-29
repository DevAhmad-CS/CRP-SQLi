/**
 * Gradient Animation
 * Animated gradients for buttons and backgrounds
 * Creates smooth color transitions
 */

document.addEventListener('DOMContentLoaded', function() {
    initGradientAnimations();
});

/**
 * Initialize gradient animations
 */
function initGradientAnimations() {
    // Animate button gradients
    const buttons = document.querySelectorAll('.btn-primary');
    
    buttons.forEach(button => {
        // Create animated gradient background
        let angle = 0;
        
        function animateGradient() {
            angle = (angle + 0.5) % 360;
            
            // Create gradient with moving angle
            button.style.background = `
                linear-gradient(${angle}deg, 
                    #9d7aff 0%, 
                    #7c5aff 50%, 
                    #9d7aff 100%
                )
            `;
            
            requestAnimationFrame(animateGradient);
        }
        
        // Start animation only when button is visible
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateGradient();
                    observer.unobserve(button);
                }
            });
        }, { threshold: 0.1 });
        
        observer.observe(button);
    });
    
    // Animate hero section gradient (if exists)
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        let angle = 0;
        
        function animateHeroGradient() {
            angle = (angle + 0.3) % 360;
            
            // Subtle gradient animation for hero background
            const gradient = `
                radial-gradient(
                    ellipse at ${50 + Math.sin(angle * Math.PI / 180) * 10}% ${50 + Math.cos(angle * Math.PI / 180) * 10}%,
                    rgba(157, 122, 255, 0.1) 0%,
                    transparent 70%
                )
            `;
            
            // Apply as overlay (preserve existing background)
            heroSection.style.backgroundImage = gradient;
            
            requestAnimationFrame(animateHeroGradient);
        }
        
        // Start animation
        animateHeroGradient();
    }
}

