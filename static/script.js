document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('detectionForm');
    const messageInput = document.getElementById('messageInput');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');

    const resultContainer = document.getElementById('resultContainer');
    const resultContent = document.getElementById('resultContent');
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    const resultText = document.getElementById('resultText');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const message = messageInput.value.trim();
        if (!message) return;

        // UI Loading State
        btnText.classList.add('disabled');
        spinner.classList.remove('disabled');
        submitBtn.style.pointerEvents = 'none';

        // Hide previous result
        resultContainer.classList.add('hidden');

        try {
            // Add an artificial small delay to ensure the loading animation is visible (aesthetic choice)
            await new Promise(r => setTimeout(r, 600));

            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error('Server returned an error');
            }

            const data = await response.json();
            displayResult(data.is_spam);

        } catch (error) {
            console.error("Error detecting spam:", error);
            alert("Connection error. Please ensure the backend is running.");
        } finally {
            // Restore UI
            btnText.classList.remove('disabled');
            spinner.classList.add('disabled');
            submitBtn.style.pointerEvents = 'auto';
        }
    });

    function displayResult(isSpam) {
        // Reset classes
        resultContent.className = 'result-content';
        resultIcon.className = 'fa-solid';

        if (isSpam) {
            // Apply SPAM styles & wording
            resultContent.classList.add('state-spam');
            resultIcon.classList.add('fa-triangle-exclamation', 'fa-beat-fade');
            resultTitle.textContent = "Spam Detected!";
            resultText.innerHTML = "<strong>Warning:</strong> This message highly matches the profile of malicious/junk SMS. Do not interact with links or provide personal info.";
        } else {
            // Apply SAFE (Ham) styles & wording
            resultContent.classList.add('state-safe');
            resultIcon.classList.add('fa-shield-check', 'fa-bounce');
            // If fa-shield-check isn't in free FA, fallback to circle-check
            resultIcon.classList.add('fa-circle-check');
            resultTitle.textContent = "Message is Safe";
            resultText.textContent = "This appears to be a normal text message. No phishing or spam signatures were currently detected.";
        }

        // Reveal the result container smoothly
        resultContainer.classList.remove('hidden');

        // Scroll slightly down if on mobile
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
