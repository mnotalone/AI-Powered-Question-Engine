const express = require('express');
const fetch = require('node-fetch'); // or built-in fetch in newer Node
const app = express();
app.use(express.json());
app.use(express.static('public')); // serve index.html from ./public

const PORT = process.env.PORT || 3000;

// Example environment variables you'll set on Render:
// HF_API_KEY, HF_MODEL

app.post('/api/ask', async (req, res) => {
  try {
    const { question } = req.body;
    if (!question) return res.status(400).send('Question required');

    // Using Hugging Face Inference API
    const HF_API_KEY = process.env.HF_API_KEY;
    const MODEL = process.env.HF_MODEL || 'microsoft/DialoGPT-medium'; // Better conversational model

    if (!HF_API_KEY) {
      return res.json({ answer: "Mock response: This is a test answer. Please set HF_API_KEY for real AI responses." });
    }

    const hfRes = await fetch(`https://api-inference.huggingface.co/models/${MODEL}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${HF_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        inputs: question,
        parameters: {
          max_length: 100, // Limit response length
          temperature: 0.7 // Add some creativity
        },
        options: { wait_for_model: true }
      })
    });

    if (!hfRes.ok) {
      const txt = await hfRes.text();
      return res.status(502).send(`Provider error: ${txt}`);
    }

    const json = await hfRes.json();
    // Extract answer from HF response
    let answer = '';
    if (Array.isArray(json) && json[0] && json[0].generated_text) {
      answer = json[0].generated_text;
    } else if (json.generated_text) {
      answer = json.generated_text;
    } else {
      answer = JSON.stringify(json);
    }

    // Clean up the answer (remove the original question if repeated)
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
