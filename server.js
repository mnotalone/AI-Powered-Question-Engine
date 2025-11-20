const express = require('express');
const fetch = require('node-fetch'); // If Node >= 18, you can use built-in fetch
const app = express();

app.use(express.json());
app.use(express.static('public')); // Serve index.html, CSS, JS

const PORT = process.env.PORT || 3000;

// POST /api/ask endpoint
app.post('/api/ask', async (req, res) => {
  try {
    const { question } = req.body;
    if (!question) return res.status(400).send('Question required');

    const HF_API_KEY = process.env.HF_API_KEY;
    const MODEL = process.env.HF_MODEL || 'microsoft/DialoGPT-medium';

    // If API key not set, return mock response
    if (!HF_API_KEY) {
      return res.json({
        answer: "Mock response: This is a test answer. Set HF_API_KEY for real AI responses."
      });
    }

    // Use the new Hugging Face Router API
    const hfRes = await fetch(`https://router.huggingface.co/models/${MODEL}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${HF_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        inputs: question,
        parameters: {
          max_new_tokens: 100, // Replaces max_length
          temperature: 0.7
        },
        options: { wait_for_model: true }
      })
    });

    if (!hfRes.ok) {
      const txt = await hfRes.text();
      return res.status(502).send(`Provider error: ${txt}`);
    }

    const json = await hfRes.json();

    // Router API returns array with 'generated_text'
    let answer = '';
    if (Array.isArray(json) && json[0]?.generated_text) {
      answer = json[0].generated_text;
    } else if (json.generated_text) {
      answer = json.generated_text;
    } else {
      answer = JSON.stringify(json);
    }

    // Remove repeated question if present
    if (answer.startsWith(question)) {
      answer = answer.substring(question.length).trim();
    }

    return res.json({ answer });

  } catch (err) {
    console.error(err);
    return res.status(500).send('Server error: ' + err.message);
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});

app.get('/env-test', (req, res) => {
  res.json({
    HF_API_KEY: !!process.env.HF_API_KEY ? 'SET' : 'NOT SET',
    HF_MODEL: process.env.HF_MODEL || 'Default: microsoft/DialoGPT-medium'
  });
});