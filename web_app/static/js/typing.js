/**
 * Typing Animation - Shared function for all pages
 * Repeats every 15 seconds
 */

document.addEventListener('DOMContentLoaded', function() {
    initTypingAnimation();
    
    // Repeat animation every 15 seconds
    setInterval(function() {
        initTypingAnimation();
    }, 15000);
});

/**
 * Initialize typing animation for elements with typing-text class
 */
function initTypingAnimation() {
    const typingElements = document.querySelectorAll('.typing-text');
    typingElements.forEach(element => {
        // Store original text if not already stored
        if (!element.dataset.originalText) {
            element.dataset.originalText = element.textContent.trim();
        }
        
        const text = element.dataset.originalText;
        if (!text) return;
        
        // Clear current content
        element.textContent = '';
        const cursor = document.createElement('span');
        cursor.className = 'cursor-blink';
        cursor.textContent = '|';
        element.appendChild(cursor);
        
        let index = 0;
        function type() {
            if (index < text.length) {
                element.insertBefore(document.createTextNode(text.charAt(index)), cursor);
                index++;
                setTimeout(type, 100);
            } else {
                cursor.style.animation = 'blink 1s infinite';
            }
        }
        type();
    });
}

