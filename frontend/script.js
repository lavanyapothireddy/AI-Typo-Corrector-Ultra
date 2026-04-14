async function correctText() {
    const text = document.getElementById("inputText").value;
    const outputDiv = document.getElementById("output");
    const totalWordsSpan = document.getElementById("totalWords");
    const wrongWordsSpan = document.getElementById("wrongWords");
    const scoreSpan = document.getElementById("score");

    // 1. YOUR RENDER URL (Update this!)
    const API_URL = "https://ai-typo-corrector-ultra.onrender.com/correct";

    if (!text.trim()) {
        outputDiv.innerText = "Please enter some text first!";
        return;
    }

    // Show loading state
    outputDiv.innerText = "AI is analyzing your text...";
    outputDiv.style.color = "#94a3b8"; // Gray color while loading

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        .then(response => response.json())
            .then(data => {
                console.log("Success:", data);
    // Use 'corrected' because that is what your Python return statement uses
    document.getElementById("output-box").innerText = data.corrected; 
})
        // 2. Update the Output Box
        outputDiv.innerText = data.corrected;
        outputDiv.style.color = "#4ade80"; // Turn green when finished

        // 3. Update Statistics
        const wordCount = text.trim().split(/\s+/).length;
        totalWordsSpan.innerText = `${wordCount} words`;
        
        // Use the error count from backend
        const errors = data.error_count || 0;
        wrongWordsSpan.innerText = `${errors} errors found`;

        // Calculate Accuracy Score
        const accuracy = data.corrected.toLowerCase() === text.toLowerCase() ? 100 : 85;
        scoreSpan.innerText = `${accuracy}% Accuracy`;

    } catch (error) {
        console.error("Error:", error);
        outputDiv.innerText = "Error: Backend is waking up. Please try again in 10 seconds.";
        outputDiv.style.color = "#f87171"; // Red for error
    }
}

// Function for the Copy Button
function copyToClipboard() {
    const text = document.getElementById("output").innerText;
    if (text && text !== "Corrected text will appear here..." && text !== "AI is analyzing your text...") {
        navigator.clipboard.writeText(text);
        alert("Copied to clipboard!");
    } else {
        alert("Nothing to copy yet!");
    }
}
