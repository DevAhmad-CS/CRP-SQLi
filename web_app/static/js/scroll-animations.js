/**
 * Scroll Animations - Intersection Observer for scroll-triggered animations
 * Animates elements when they come into viewport
 */

document.addEventListener('DOMContentLoaded', function() {
    initScrollAnimations();
});

/**
 * Initialize scroll animations using Intersection Observer
 */
function initScrollAnimations() {
    // Improved animation options for better timing
    const observerOptions = {
        threshold: 0.15,  // Trigger when 15% of element is visible (was 0.1)
        rootMargin: '0px 0px -80px 0px'  // Start animation 80px before element enters viewport (was -50px)
    };
    
    // Track scroll direction for one-way animation (only on scroll down)
    let lastScrollY = window.scrollY || window.pageYOffset;
    let isScrollingDown = true;
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY || window.pageYOffset;
        isScrollingDown = currentScrollY > lastScrollY;
        lastScrollY = currentScrollY;
    }, { passive: true });
    
    // Create observer - only animate on scroll down
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach((entry) => {
            const element = entry.target;
            
            // Always animate when element enters viewport (for initial load and scroll down)
            if (entry.isIntersecting) {
                // Element entered viewport - show animation
                // IMPORTANT: Only animate individual elements, NOT containers
                // Get position index within its container for staggered effect
                const container = element.parentElement;
                // Filter to get only animated elements (not containers like .stats-grid, .info-grid, etc.)
                const siblings = Array.from(container.children).filter(child => {
                    // Only include actual animated elements, exclude containers
                    return (child.classList.contains('stat-card') || 
                            child.classList.contains('info-item') || 
                            child.classList.contains('tech-item') || 
                            child.classList.contains('example-card') ||
                            child.classList.contains('about-section')) &&
                           // Exclude containers
                           !child.classList.contains('stats-grid') &&
                           !child.classList.contains('info-grid') &&
                           !child.classList.contains('tech-grid') &&
                           !child.classList.contains('examples-grid') &&
                           !child.classList.contains('examples-category');
                });
                const index = siblings.indexOf(element);
                
                // Calculate delay based on element type and position
                let delay = 0;
                
                if (element.classList.contains('stat-card')) {
                    delay = index * 60;  // Fast stagger
                } else if (element.classList.contains('about-section')) {
                    delay = index * 100;  // Slower stagger
                } else if (element.classList.contains('tech-item')) {
                    delay = index * 80;  // Medium stagger
                } else if (element.classList.contains('example-card')) {
                    delay = index * 90;  // Smooth stagger
                } else if (element.classList.contains('info-item')) {
                    delay = index * 70;  // Fast stagger
                } else {
                    delay = index * 80;  // Default
                }
                
                // Apply animation with stagger delay using requestAnimationFrame for better performance
                const animateElement = () => {
                    element.style.opacity = '1';
                    // Get final transform based on animation type
                    const animType = element.dataset.animationType || 'fadeInUp';
                    if (animType === 'scaleIn') {
                        element.style.transform = 'scale(1)';
                    } else if (animType === 'fadeInLeft') {
                        element.style.transform = 'translateX(0)';
                    } else if (animType === 'fadeInRight') {
                        element.style.transform = 'translateX(0)';
                    } else {
                        element.style.transform = 'translateY(0)';
                    }
                };
                
                // Use requestAnimationFrame for better performance
                if (delay === 0) {
                    requestAnimationFrame(animateElement);
                } else {
                    setTimeout(() => {
                        requestAnimationFrame(animateElement);
                    }, delay);
                }
                
            } else {
                // Element left viewport - only hide if scrolling up
                const currentScrollY = window.scrollY || window.pageYOffset;
                const wasScrollingUp = currentScrollY < lastScrollY;
                
                // Only hide when scrolling up
                if (wasScrollingUp) {
                    const animType = element.dataset.animationType || 'fadeInUp';
                    element.style.opacity = '0';
                    
                    // Reset to initial transform based on animation type
                    if (animType === 'scaleIn') {
                        element.style.transform = 'scale(0.9)';
                    } else if (animType === 'fadeInLeft') {
                        element.style.transform = 'translateX(-30px)';
                    } else if (animType === 'fadeInRight') {
                        element.style.transform = 'translateX(30px)';
                    } else {
                        element.style.transform = 'translateY(30px)';
                    }
                }
            }
        });
    }, observerOptions);
    
    // Elements to animate on scroll - ONLY individual elements, NOT containers
    // Containers like .stats-grid, .info-grid, .tech-grid, .examples-grid should NOT be animated
    const animatedElements = document.querySelectorAll(
        '.stat-card, .info-item, .tech-item, .about-section, .example-card'
    );
    
    // Ensure containers are NOT animated - only fade for info-section and performance-note
    const containers = document.querySelectorAll(
        '.stats-grid, .info-grid, .tech-grid, .examples-grid, .examples-category, .examples-section'
    );
    containers.forEach(container => {
        // Make sure containers don't have animation styles
        container.style.opacity = '1';
        container.style.transform = 'none';
        container.style.transition = 'none';
    });
    
    // Add fade animation for info-section and performance-note containers
    const fadeContainers = document.querySelectorAll('.info-section, .performance-note');
    fadeContainers.forEach(container => {
        // Check if container is already in viewport
        const rect = container.getBoundingClientRect();
        const isInViewport = rect.top < window.innerHeight && rect.bottom > 0;
        
        if (isInViewport) {
            // Container is already visible - show it immediately
            container.style.opacity = '1';
            container.style.transition = 'none';
        } else {
            // Simple fade animation for containers
            container.style.opacity = '0';
            container.style.transition = 'opacity 0.6s ease-out';
        }
        
        const fadeObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                } else {
                    // Only hide if scrolling up
                    const currentScrollY = window.scrollY || window.pageYOffset;
                    const wasScrollingUp = currentScrollY < lastScrollY;
                    if (wasScrollingUp) {
                        entry.target.style.opacity = '0';
                    }
                }
            });
        }, { threshold: 0.1 });
        
        fadeObserver.observe(container);
    });
    
    // Set initial state and observe with different animation types
    animatedElements.forEach((element, idx) => {
        // Check if element already has CSS animation
        const hasAnimation = getComputedStyle(element).animationName !== 'none';
        
        if (!hasAnimation) {
            // Determine animation type based on element class
            let animationType = 'fadeInUp'; // default
            let initialTransform = 'translateY(30px)';
            
            if (element.classList.contains('stat-card')) {
                // Alternate between left and right for stat cards
                animationType = idx % 2 === 0 ? 'fadeInLeft' : 'fadeInRight';
                initialTransform = idx % 2 === 0 ? 'translateX(-30px)' : 'translateX(30px)';
            } else if (element.classList.contains('info-item')) {
                // Alternate between left and right for info items
                animationType = idx % 2 === 0 ? 'fadeInLeft' : 'fadeInRight';
                initialTransform = idx % 2 === 0 ? 'translateX(-30px)' : 'translateX(30px)';
            } else if (element.classList.contains('about-section')) {
                // Alternate between left and right for sections
                animationType = idx % 2 === 0 ? 'fadeInLeft' : 'fadeInRight';
                initialTransform = idx % 2 === 0 ? 'translateX(-30px)' : 'translateX(30px)';
            } else if (element.classList.contains('tech-item')) {
                animationType = 'fadeInUp';
                initialTransform = 'translateY(30px)';
            } else if (element.classList.contains('example-card')) {
                animationType = 'fadeInUp';
                initialTransform = 'translateY(30px)';
            }
            
            // Store animation type for later use
            element.dataset.animationType = animationType;
            
            // Determine easing function and duration based on element type
            let easingFunction = 'cubic-bezier(0.4, 0, 0.2, 1)'; // default
            let duration = 0.7; // default
            
            if (element.classList.contains('stat-card')) {
                easingFunction = 'cubic-bezier(0.34, 1.56, 0.64, 1)'; // Bounce effect
                duration = 0.6; // Faster
            } else if (element.classList.contains('example-card')) {
                easingFunction = 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'; // Smooth ease-out
                duration = 0.8; // Medium
            } else if (element.classList.contains('about-section')) {
                easingFunction = 'cubic-bezier(0.4, 0, 0.2, 1)'; // Standard
                duration = 1.0; // Slower for emphasis
            } else if (element.classList.contains('tech-item')) {
                easingFunction = 'cubic-bezier(0.25, 0.1, 0.25, 1)'; // Ease-in-out
                duration = 0.7; // Medium
            } else if (element.classList.contains('info-item')) {
                easingFunction = 'cubic-bezier(0.4, 0, 1, 1)'; // Ease-out
                duration = 0.6; // Faster
            }
            
            // Store easing and duration for later use
            element.dataset.easing = easingFunction;
            element.dataset.duration = duration;
            
            // Set initial hidden state for scroll animation
            // Check if element is already in viewport - if yes, show it immediately
            const rect = element.getBoundingClientRect();
            const isInViewport = rect.top < window.innerHeight && rect.bottom > 0;
            
            if (isInViewport) {
                // Element is already visible - show it immediately without animation
                element.style.opacity = '1';
                if (animationType === 'scaleIn') {
                    element.style.transform = 'scale(1)';
                } else if (animationType === 'fadeInLeft' || animationType === 'fadeInRight') {
                    element.style.transform = 'translateX(0)';
                } else {
                    element.style.transform = 'translateY(0)';
                }
                element.style.transition = 'none'; // No transition for initial visible elements
            } else {
                // Element is not visible - set initial hidden state
                element.style.opacity = '0';
                element.style.transform = initialTransform;
                element.style.transition = `opacity ${duration}s ${easingFunction}, transform ${duration}s ${easingFunction}`;
            }
        }
        
        // Observe element
        observer.observe(element);
    });
}

