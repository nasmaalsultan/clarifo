document.addEventListener('DOMContentLoaded', function() {
    const checkBtn = document.getElementById('check-btn');
    const statementInput = document.getElementById('statement');
    const resultsPlaceholder = document.getElementById('results-placeholder');
    const resultsContent = document.getElementById('results-content');
    const loadingIndicator = document.getElementById('loading');
    const accuracyValue = document.getElementById('accuracy-value');
    const accuracyMeter = document.getElementById('accuracy-meter');
    const accuracyVerdict = document.getElementById('accuracy-verdict');
    const sourcesCount = document.getElementById('sources-count');
    const processingTime = document.getElementById('processing-time');
    const complexity = document.getElementById('complexity');
    const sourcesContainer = document.getElementById('sources-container');
    const termAnalysis = document.getElementById('term-analysis');
    const termsContainer = document.getElementById('terms-container');

    checkBtn.addEventListener('click', function() {
        const statement = statementInput.value.trim();

        if (!statement) {
            alert('Please enter a statement to check.');
            return;
        }

        // Show loading indicator
        loadingIndicator.style.display = 'block';
        resultsPlaceholder.style.display = 'none';
        resultsContent.style.display = 'none';
        termAnalysis.style.display = 'none';

        // Send request to backend
        // Update the fetch call in the checkBtn event listener
        fetch('/check_fact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ statement: statement })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide loading indicator
            loadingIndicator.style.display = 'none';

            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }

            // Show results
            resultsContent.style.display = 'block';

            // Update UI with results
            updateResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            loadingIndicator.style.display = 'none';
            alert('The fact-checking service is currently unavailable. Please try again in a moment.');
        });
    });

    function updateResults(data) {
        // Update accuracy display
        const accuracyPercent = Math.round(data.accuracy * 100);
        accuracyValue.textContent = `${accuracyPercent}%`;

        // Animate the accuracy meter
        const circumference = 565.48; // 2 * π * r (r=90)
        const offset = circumference - (data.accuracy * circumference);
        accuracyMeter.style.strokeDashoffset = offset;

        // Update verdict
        if (data.accuracy >= 0.8) {
            accuracyVerdict.textContent = "Mostly True";
            accuracyVerdict.className = "accuracy-verdict verdict-true";
        } else if (data.accuracy >= 0.6) {
            accuracyVerdict.textContent = "Partially True";
            accuracyVerdict.className = "accuracy-verdict verdict-mixed";
        } else if (data.accuracy >= 0.4) {
            accuracyVerdict.textContent = "Partially False";
            accuracyVerdict.className = "accuracy-verdict verdict-mixed";
        } else {
            accuracyVerdict.textContent = "Mostly False";
            accuracyVerdict.className = "accuracy-verdict verdict-false";
        }

        // Update other details
        sourcesCount.textContent = data.sources_analyzed;
        processingTime.textContent = `${data.processing_time}s`;
        complexity.textContent = data.complexity;

        // Populate sources
        sourcesContainer.innerHTML = '';
        if (data.sources && data.sources.length > 0) {
            data.sources.forEach(source => {
                const sourceElement = document.createElement('div');
                sourceElement.className = 'source-item';

                const confidenceClass = source.confidence > 0.85 ? 'high-confidence' :
                                       source.confidence > 0.7 ? 'medium-confidence' : 'low-confidence';

                sourceElement.innerHTML = `
                    <i class="fas fa-file-alt"></i>
                    <div style="flex-grow: 1;">
                        <div style="display: flex; justify-content: space-between;">
                            <span><a href="${source.url}" target="_blank">${source.name}</a></span>
                            <span>${Math.round(source.confidence * 100)}% match</span>
                        </div>
                        <div class="confidence-bar">
                            <div class="confidence-fill ${confidenceClass}" style="width: ${source.confidence * 100}%"></div>
                        </div>
                    </div>
                `;

                sourcesContainer.appendChild(sourceElement);
            });
        } else {
            sourcesContainer.innerHTML = '<p>No sources available for analysis.</p>';
        }

        // Show term analysis if available
        if (data.analysis_details && data.analysis_details.term_analysis) {
            termAnalysis.style.display = 'block';
            termsContainer.innerHTML = '';

            data.analysis_details.term_analysis.key_terms.forEach(term => {
                const termElement = document.createElement('span');
                termElement.className = 'term-item';
                termElement.innerHTML = `${term.term} <span class="term-score">(${term.score.toFixed(2)})</span>`;
                termsContainer.appendChild(termElement);
            });
        }
    }

    // Initialize with a sample statement for demonstration
    statementInput.value = "The Earth revolves around the Sun.";
});