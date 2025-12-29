// Main JavaScript for the application

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('queryForm');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const query = document.getElementById('query').value;
            
            if (!query.trim()) {
                alert('Please enter a SQL query');
                return;
            }
            
            // Show loading (skeleton or spinner), hide result
            loading.classList.remove('hidden');
            result.classList.add('hidden');
            
            // Use skeleton loader if available
            if (typeof showSkeletonLoader === 'function') {
                showSkeletonLoader(loading);
            }
            
            try {
                const formData = new FormData();
                formData.append('query', query);
                
                const response = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    displayResult(data);
                } else {
                    showError(data.error || 'An error occurred');
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            } finally {
                // Hide loading (skeleton or spinner)
                if (typeof hideSkeletonLoader === 'function') {
                    hideSkeletonLoader(loading);
                } else {
                    loading.classList.add('hidden');
                }
            }
        });
    }
});

function displayResult(data) {
    const resultDiv = document.getElementById('result');
    const isMalicious = data.is_malicious;
    
    resultDiv.className = `result ${isMalicious ? 'malicious' : 'normal'}`;
    resultDiv.classList.remove('hidden');
    
    const icon = isMalicious ? '⚠️' : '✅';
    const title = isMalicious ? 'SQL Injection Detected!' : 'Normal Query';
    
    resultDiv.innerHTML = `
        <h3>${icon} ${title}</h3>
        <div class="result-details">
            <p><strong>Query:</strong> <code>${escapeHtml(data.query)}</code></p>
            <p><strong>Prediction:</strong> ${data.prediction}</p>
            <p><strong>Confidence:</strong> ${data.confidence}%</p>
            
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: ${data.confidence}%">
                    ${data.confidence}%
                </div>
            </div>
            
            <div class="probabilities">
                <div class="prob-item">
                    <strong>Normal</strong>
                    <span>${data.probabilities.normal}%</span>
                </div>
                <div class="prob-item">
                    <strong>Malicious</strong>
                    <span>${data.probabilities.malicious}%</span>
                </div>
            </div>
        </div>
    `;
    
    // Animate confidence bar using progress bar animation
    setTimeout(() => {
        const confidenceFill = resultDiv.querySelector('.confidence-fill');
        if (confidenceFill && typeof animateProgressBar === 'function') {
            animateProgressBar(confidenceFill, data.confidence, 1200);
        } else {
            // Fallback if animation function not available
            confidenceFill.style.width = `${data.confidence}%`;
        }
    }, 100);
    
    // Scroll to result
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(message) {
    const resultDiv = document.getElementById('result');
    resultDiv.className = 'result malicious';
    resultDiv.classList.remove('hidden');
    resultDiv.innerHTML = `
        <h3 style="color: #d32f2f;">❌ Error</h3>
        <p>${escapeHtml(message)}</p>
    `;
}

function clearForm() {
    document.getElementById('query').value = '';
    document.getElementById('result').classList.add('hidden');
}

function fillExample(button) {
    const exampleCard = button.closest('.example-card');
    const codeElement = exampleCard.querySelector('code');
    const queryText = codeElement.textContent;
    
    document.getElementById('query').value = queryText;
    document.getElementById('query').focus();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
