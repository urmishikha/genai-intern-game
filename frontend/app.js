document.addEventListener('DOMContentLoaded', () => {
    const guessInput = document.getElementById('guess-input');
    const submitButton = document.getElementById('submit-guess');
    const messageDiv = document.getElementById('message');
    const scoreDiv = document.getElementById('score');
    const guessHistory = document.getElementById('guess-history');
    const globalCountDiv = document.getElementById('global-count');
    const personaSelect = document.getElementById('persona-select');
    const currentWordSpan = document.getElementById('current-word');

    let currentWord = 'Rock';
    let score = 0;

    submitButton.addEventListener('click', submitGuess);
    guessInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') submitGuess();
    });

async function submitGuess() {
  const guess = guessInput.value.trim();
  if (!guess) return;

  try {
    const response = await axios.post(
      'http://localhost:8000/api/guess',
      {
        word: currentWord,
        guess: guess,
        persona: document.getElementById('persona-select').value
      },
      {
        headers: { 'Content-Type': 'application/json' }
      }
    );

    // Update UI only if response is valid
    if (response.data && response.data.status === 'success') {
      currentWord = guess;
      document.getElementById('current-word').textContent = currentWord;
      document.getElementById('score').textContent = `Score: ${response.data.score}`;
      updateHistory(response.data.history);
      showMessage(response.data.message, 'success');
    } else {
      showMessage(response.data?.message || 'Invalid response', 'error');
    }
  } catch (error) {
    console.error('API Error:', error);
    showMessage(error.response?.data?.detail || 'Failed to submit guess', 'error');
  }
}
    function showMessage(message, type) {
        messageDiv.textContent = message;
        messageDiv.className = type;
    }

    function updateHistory(history) {
        guessHistory.innerHTML = '';
        history.slice().reverse().forEach(guess => {
            const li = document.createElement('li');
            li.textContent = guess;
            guessHistory.appendChild(li);
        });
    }

    // Load initial history
    async function loadHistory() {
        try {
            const response = await axios.get('/api/history');
            updateHistory(response.data.history);
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    loadHistory();
});