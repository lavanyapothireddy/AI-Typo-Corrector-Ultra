#!/bin/bash
echo "Injecting API key..."
sed -i "s/GROQ_KEY_PLACEHOLDER/$GROQ_API_KEY/g" js/app.js
echo "✅ Done"
