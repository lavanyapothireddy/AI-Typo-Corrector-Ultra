#!/bin/bash
# Replace placeholder in app.js with the real key from environment
sed -i "s|window.__GROQ_KEY__ || ''|'$GROQ_API_KEY'|g" js/app.js
echo "✅ API key injected successfully"
