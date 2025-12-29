/**
 * Loading Skeleton Animation
 * Professional skeleton loading effect instead of spinner
 * Creates shimmer animation for loading states
 */

/**
 * Create skeleton loader element
 * @param {string} type - Type of skeleton ('text', 'card', 'bar')
 * @param {object} options - Options for skeleton (width, height, etc.)
 * @returns {HTMLElement} Skeleton element
 */
function createSkeleton(type = 'text', options = {}) {
    const skeleton = document.createElement('div');
    skeleton.className = 'skeleton-loader';
    
    // Default options
    const defaultOptions = {
        width: type === 'text' ? '100%' : type === 'bar' ? '100%' : '100%',
        height: type === 'text' ? '1rem' : type === 'bar' ? '0.5rem' : '200px',
        borderRadius: type === 'card' ? '12px' : '4px',
        margin: type === 'text' ? '0.5rem 0' : '0'
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    // Apply styles
    skeleton.style.cssText = `
        width: ${finalOptions.width};
        height: ${finalOptions.height};
        background: linear-gradient(
            90deg,
            rgba(157, 122, 255, 0.1) 0%,
            rgba(157, 122, 255, 0.2) 50%,
            rgba(157, 122, 255, 0.1) 100%
        );
        background-size: 200% 100%;
        border-radius: ${finalOptions.borderRadius};
        margin: ${finalOptions.margin};
        animation: skeleton-shimmer 1.5s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    `;
    
    return skeleton;
}

/**
 * Create skeleton structure for result loading
 * @returns {HTMLElement} Skeleton container
 */
function createResultSkeleton() {
    const container = document.createElement('div');
    container.className = 'skeleton-container';
    container.style.cssText = `
        padding: 2rem;
        background: rgba(15, 15, 15, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        margin-top: 2rem;
        border: 2px dashed rgba(157, 122, 255, 0.3);
    `;
    
    // Title skeleton
    const titleSkeleton = createSkeleton('text', { width: '60%', height: '2rem', margin: '0 0 1.5rem 0' });
    container.appendChild(titleSkeleton);
    
    // Text lines skeleton
    for (let i = 0; i < 3; i++) {
        const lineSkeleton = createSkeleton('text', { 
            width: i === 2 ? '80%' : '100%', 
            height: '1rem',
            margin: '0.75rem 0'
        });
        container.appendChild(lineSkeleton);
    }
    
    // Bar skeleton
    const barSkeleton = createSkeleton('bar', { 
        width: '100%', 
        height: '0.5rem',
        margin: '1.5rem 0 0 0',
        borderRadius: '4px'
    });
    container.appendChild(barSkeleton);
    
    return container;
}

/**
 * Add skeleton shimmer animation to CSS if not exists
 */
function addSkeletonAnimation() {
    // Check if animation already exists
    if (document.getElementById('skeleton-animation-style')) return;
    
    const style = document.createElement('style');
    style.id = 'skeleton-animation-style';
    style.textContent = `
        @keyframes skeleton-shimmer {
            0% {
                background-position: -200% 0;
            }
            100% {
                background-position: 200% 0;
            }
        }
        
        .skeleton-loader {
            will-change: background-position;
        }
    `;
    document.head.appendChild(style);
}

/**
 * Initialize skeleton loading
 */
function initSkeletonLoading() {
    addSkeletonAnimation();
}

/**
 * Show skeleton loader instead of spinner
 * @param {HTMLElement} container - Container to show skeleton in
 */
function showSkeletonLoader(container) {
    if (!container) return;
    
    // Clear existing content
    container.innerHTML = '';
    
    // Create and append skeleton
    const skeleton = createResultSkeleton();
    container.appendChild(skeleton);
    container.classList.remove('hidden');
}

/**
 * Hide skeleton loader
 * @param {HTMLElement} container - Container to hide skeleton in
 */
function hideSkeletonLoader(container) {
    if (!container) return;
    container.classList.add('hidden');
    container.innerHTML = '';
}

// Initialize on load
document.addEventListener('DOMContentLoaded', function() {
    initSkeletonLoading();
});

