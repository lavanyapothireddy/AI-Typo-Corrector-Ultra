async function correctText() {
    const text = document.getElementById("inputText").value;
    if (!text.trim()) return;

    const outputDiv = document.getElementById("output");
    outputDiv.innerText = "AI is thinking...";

    try {
        const res = await fetch("https://ai-typo-corrector-ultra.onrender.com", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await res.json();
        outputDiv.innerText = data.corrected;

        // Simple accuracy logic: compare word changes
        const originalWords = text.trim().split(/\s+/);
        const correctedWords = data.corrected.trim().split(/\s+/);
        
        // Count how many words remain identical
        let matches = 0;
        originalWords.forEach((word, index) => {
            if (word === correctedWords[index]) matches++;
        });

        const total = originalWords.length;
        const accuracy = Math.round((matches / total) * 100);

        document.getElementById("totalWords").innerText = `Total Words: ${total}`;
        document.getElementById("score").innerHTML = `
            <div class="score-box">
                AI Accuracy Score: ${accuracy}%
            </div>`;

    } catch (error) {
        outputDiv.innerText = "Backend Error: Make sure your Python server is running.";
    }
}
