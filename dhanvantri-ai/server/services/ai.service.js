const aiClient = require('./aiClient');

// ─── Safe Medical Prompt Template ─────────────────────────
const buildMedicalPrompt = (userInput) => {
  return `You are Dhanvantri, a helpful AI health assistant. 

STRICT RULES:
- Never provide a medical diagnosis
- Never prescribe medications or treatments  
- Always recommend consulting a healthcare professional
- Only provide general health information and observations
- Always include a disclaimer in your response

User input: "${userInput}"

Respond with a JSON object in this exact format:
{
  "observations": "General observations about the symptoms mentioned",
  "possibleFactors": ["factor1", "factor2", "factor3"],
  "generalAdvice": "General wellness advice only",
  "urgencyLevel": "low|medium|high",
  "disclaimer": "This is not a medical diagnosis. Please consult a healthcare professional.",
  "confidence": 0.0
}`;
};

// ─── Analyze Text with AI ──────────────────────────────────
const analyzeWithAI = async (userInput) => {
  try {
    const completion = await aiClient.chat.completions.create({
      model: 'grok-3-mini',
      messages: [
        {
          role: 'system',
          content: 'You are a safe, helpful health information assistant. You never diagnose or prescribe. Always respond in valid JSON only.',
        },
        {
          role: 'user',
          content: buildMedicalPrompt(userInput),
        },
      ],
      max_tokens: 1000,
      temperature: 0.3,
    });

    // Extract response text
    const responseText = completion.choices[0].message.content;

    // Parse JSON response
    const cleanedResponse = responseText.replace(/```json|```/g, '').trim();
    const parsed = JSON.parse(cleanedResponse);

    return {
      success: true,
      data: parsed,
    };

  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
};

module.exports = { analyzeWithAI };