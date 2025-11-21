const askBtn = document.getElementById('askBtn');
const qInput = document.getElementById('q');
const answerEl = document.getElementById('answer');
const statusEl = document.getElementById('status');

askBtn.addEventListener('click', async () => {
  const question = qInput.value.trim();
  if (!question) {
    answerEl.textContent = 'Please type a question.';
    statusEl.textContent = '';
    return;
  }

  statusEl.textContent = 'Sending question to AI...';
  answerEl.textContent = '';
  askBtn.disabled = true;
  askBtn.textContent = 'Processing...';

  try {
    const res = await fetch('/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });

    const data = await res.json();
    answerEl.textContent = data.answer ?? 'No answer returned';
    statusEl.textContent = 'Answer received!';
  } catch (err) {
    statusEl.textContent = 'Network or server error';
    answerEl.textContent = err.message || String(err);
  } finally {
    askBtn.disabled = false;
    askBtn.textContent = 'Ask AI';
  }
});

// Allow Enter key to submit
qInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') askBtn.click();
});
