const express = require('express');
const fetch = require('node-fetch'); // or use built-in fetch in Node 18+
const app = express();
app.use(express.json());
app.use(express.static('public')); // serve index.html and assets

const PORT = process.env.PORT || 3000;

// Hugging Face environment variables
const HF_API_KEY = process.env.HF_API_KEY;
const MODEL = process.env.HF_MODEL || 'microsoft/DialoGPT-medium';

app.post('/api/ask', async (req, res) => {
  try {
    const { question } = req.body;
    if (!question) return res.status(400).send('Question required');

    // If HF_API_KEY is not set, return mock response
    if (!HF_API_KEY) {
      return res.json({
        answer: "Mock response: This is a test answer. Please set HF_API_KEY for real AI responses."
      });
    }

    // Call the Hugging Face router API
    const hfRes = await fetch(`https://router.huggingface.co/models/${MODEL}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${HF_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        inputs: question,
        parameters: {
          max_new_tokens: 100, // limits response length
          temperature: 0.7
        }
      })
    });

    if (!hfRes.ok) {
      const txt = await hfRes.text();
      return res.status(502).send(`Provider error: ${txt}`);
    }

    const json = await hfRes.json();

    // Hugging Face router returns text in different formats
    let answer = '';
    if (Array.isArray(json) && json[0] && json[0].generated_text) {
      answer = json[0].generated_text;
    } else if (json.generated_text) {
      answer = json.generated_text;
    } else {
      answer = JSON.stringify(json);
    }

    // Remove the question if repeated
    if (answer.startsWith(question)) {
      answer = answer.substring(question.length).trim();
    }

    return res.json({ answer });
  } catch (err) {
    console.error(err);
    return res.status(500).send('Server error: ' + err.message);
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
