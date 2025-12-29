/**
 * Reveal Text Animation
 * Text reveals character by character or word by word
 * Creates professional text entrance effect
 */

document.addEventListener('DOMContentLoaded', function() {
    initRevealText();
});

/**
 * Initialize reveal text animation
 */
function initRevealText() {
    // Target elements with reveal-text class
    const revealElements = document.querySelectorAll('.reveal-text');
    
    if (revealElements.length === 0) return;
    
    // Create Intersection Observer
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                // Only animate once
                if (!element.dataset.revealed) {
                    revealText(element);
                    element.dataset.revealed = 'true';
                    observer.unobserve(element);
                }
            }
        });
    }, observerOptions);
    
    // Observe all reveal elements
    revealElements.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Reveal text character by character or word by word
 * @param {HTMLElement} element - Element containing text
 */
function revealText(element) {
    const originalText = element.textContent.trim();
    const words = originalText.split(' ');
    const isWordByWord = element.dataset.revealType === 'word' || words.length < 10;
    
    // Clear element
    element.textContent = '';
    element.style.opacity = '1';
    
    if (isWordByWord) {
        // Reveal word by word
        revealWords(element, words, 0);
    } else {
        // Reveal character by character
        revealCharacters(element, originalText, 0);
    }
}

/**
 * Reveal text word by word
 */
function revealWords(element, words, index) {
    if (index >= words.length) return;
    
    const wordSpan = document.createElement('span');
    wordSpan.textContent = words[index] + (index < words.length - 1 ? ' ' : '');
    wordSpan.style.opacity = '0';
    wordSpan.style.transform = 'translateY(20px)';
    wordSpan.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
    wordSpan.style.display = 'inline-block';
    
    element.appendChild(wordSpan);
    
    // Animate word in
    requestAnimationFrame(() => {
        wordSpan.style.opacity = '1';
        wordSpan.style.transform = 'translateY(0)';
    });
    
    // Continue with next word
    setTimeout(() => {
        revealWords(element, words, index + 1);
    }, 80); // Delay between words
}

/**
 * Reveal text character by character
 */
function revealCharacters(element, text, index) {
    if (index >= text.length) return;
    
    const char = text[index];
    const charSpan = document.createElement('span');
    charSpan.textContent = char === ' ' ? '\u00A0' : char; // Non-breaking space for spaces
    charSpan.style.opacity = '0';
    charSpan.style.transform = 'translateY(10px)';
    charSpan.style.transition = 'opacity 0.2s ease-out, transform 0.2s ease-out';
    charSpan.style.display = 'inline-block';
    
    element.appendChild(charSpan);
    
    // Animate character in
    requestAnimationFrame(() => {
        charSpan.style.opacity = '1';
        charSpan.style.transform = 'translateY(0)';
    });
    
    // Continue with next character
    setTimeout(() => {
        revealCharacters(element, text, index + 1);
    }, 30); // Delay between characters
}

