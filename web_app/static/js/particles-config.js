/**
 * Particles.js Configuration
 * Beautiful animated background for SQL Injection Detection System
 */

document.addEventListener('DOMContentLoaded', function() {
    // Ensure particles container is properly positioned
    const particlesContainer = document.getElementById('particles-js');
    if (particlesContainer) {
        particlesContainer.style.position = 'fixed';
        particlesContainer.style.top = '0';
        particlesContainer.style.left = '0';
        particlesContainer.style.width = '100%';
        particlesContainer.style.height = '100%';
        particlesContainer.style.zIndex = '-1';
        particlesContainer.style.margin = '0';
        particlesContainer.style.padding = '0';
        particlesContainer.style.display = 'block';
    }
    
    if (typeof particlesJS !== 'undefined') {
        particlesJS('particles-js', {
            particles: {
                number: {
                    value: 80,
                    density: {
                        enable: true,
                        value_area: 800
                    }
                },
                color: {
                    value: ['#667eea', '#764ba2', '#f093fb', '#4facfe']
                },
                shape: {
                    type: 'circle',
                    stroke: {
                        width: 0,
                        color: '#000000'
                    }
                },
                opacity: {
                    value: 0.5,
                    random: false,
                    anim: {
                        enable: false,
                        speed: 1,
                        opacity_min: 0.1,
                        sync: false
                    }
                },
                size: {
                    value: 3,
                    random: true,
                    anim: {
                        enable: false,
                        speed: 40,
                        size_min: 0.1,
                        sync: false
                    }
                },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: '#667eea',
                    opacity: 0.4,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 1,
                    direction: 'none',
                    random: true,
                    straight: false,
                    out_mode: 'out',
                    bounce: false,
                    attract: {
                        enable: true,
                        rotateX: 600,
                        rotateY: 1200
                    }
                }
            },
            interactivity: {
                detect_on: 'canvas',
                events: {
                    onhover: {
                        enable: true,
                        mode: 'grab'
                    },
                    onclick: {
                        enable: true,
                        mode: 'push'
                    },
                    resize: true
                },
                modes: {
                    grab: {
                        distance: 250,
                        line_linked: {
                            opacity: 1
                        }
                    },
                    bubble: {
                        distance: 400,
                        size: 40,
                        duration: 2,
                        opacity: 8,
                        speed: 3
                    },
                    repulse: {
                        distance: 200,
                        duration: 0.4
                    },
                    push: {
                        particles_nb: 4
                    },
                    remove: {
                        particles_nb: 2
                    }
                }
            },
            retina_detect: true
        });
        
        // After particles are initialized, ensure canvas is positioned correctly
        setTimeout(function() {
            const canvas = document.querySelector('#particles-js canvas');
            if (canvas) {
                canvas.style.position = 'fixed';
                canvas.style.top = '0';
                canvas.style.left = '0';
                canvas.style.width = '100%';
                canvas.style.height = '100%';
                canvas.style.zIndex = '-1';
                canvas.style.margin = '0';
                canvas.style.padding = '0';
                canvas.style.display = 'block';
                canvas.style.pointerEvents = 'auto';
                
                // Add mouse move event listener to whole window
                window.addEventListener('mousemove', function(e) {
                    // Trigger particles interaction by dispatching mouse event on canvas
                    const mouseEvent = new MouseEvent('mousemove', {
                        clientX: e.clientX,
                        clientY: e.clientY,
                        bubbles: true,
                        cancelable: true
                    });
                    canvas.dispatchEvent(mouseEvent);
                });
            }
            
            // Ensure particles container covers full window for mouse detection
            if (particlesContainer) {
                particlesContainer.style.pointerEvents = 'auto';
            }
        }, 200);
    }
});

