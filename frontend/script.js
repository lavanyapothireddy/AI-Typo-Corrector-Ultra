async function correctText() {
    const text = document.getElementById("inputText").value;
    const outputDiv = document.getElementById("output");
    const wordCountSpan = document.getElementById("totalWords");
    const errorCountSpan = document.getElementById("wrongWords");
    const scoreSpan = document.getElementById("score");

    if (!text.trim()) return;

    outputDiv.innerText = "AI is thinking...";

    try {
        // REPLACE THIS URL with your actual Render URL
        const res = await fetch("https://ai-typo-corrector-ultra.onrender.com", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await res.json();

        // Update the UI
        outputDiv.innerText = data.corrected;
        
        // Update Stats
        const wordCount = text.trim().split(/\s+/).length;
        wordCountSpan.innerText = `${wordCount} words`;
        errorCountSpan.innerText = `${data.error_count} errors`;
        
        // Simple Score Logic
        const accuracy = data.error_count === 0 ? 100 : 85;
        scoreSpan.innerText = `${accuracy}% Accuracy`;

    } catch (error) {
        outputDiv.innerText = "Error: Could not reach the AI server.";
        console.error("Fetch error:", error);
    }
}
