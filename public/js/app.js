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

    if (!res.ok) {
      const txt = await res.text();
      statusEl.textContent = 'Error from server';
      answerEl.textContent = txt;
      return;
    }

    const data = await res.json();
    statusEl.textContent = 'Answer received!';
    answerEl.textContent = data.answer ?? 'No answer returned';
  } catch (err) {
    statusEl.textContent = 'Network error';
    answerEl.textContent = err.message || String(err);
  } finally {
    askBtn.disabled = false;
    askBtn.textContent = 'Ask AI';
  }
});

// Allow Enter key to submit
qInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    askBtn.click();
  }
});

// Make sure fetch points to the API route correctly
async function askQuestion(question) {
  const res = await fetch('/api/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });

  if (!res.ok) {
    const text = await res.text();
    console.error("API error:", text);
    return;
  }

  const data = await res.json();
  console.log(data.answer); // display in UI
  return data.answer;
}

