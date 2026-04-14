async function correctText() {
    const text = document.getElementById("inputText").value;
    const outputDiv = document.getElementById("output");
    
    // Replace this with your actual Render URL
    const RENDER_URL = "https://your-app-name.onrender.com/correct";

    if (!text.trim()) {
        outputDiv.innerText = "Please enter some text first!";
        return;
    }

    outputDiv.innerText = "Correcting...";

    try {
        const res = await fetch(RENDER_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await res.json();

        // 1. Show the corrected text
        outputDiv.innerText = data.corrected;

        // 2. Calculate and display the stats
        const words = text.trim().split(/\s+/);
        const totalCount = words.length;
        const errorCount = data.error_count || 0;
        const score = Math.max(0, 100 - (errorCount * 10));

        // 3. Update the HTML spans
        document.getElementById("totalWords").innerText = `Total Words: ${totalCount}`;
        document.getElementById("wrongWords").innerText = `Errors: ${errorCount}`;
        document.getElementById("score").innerText = `Accuracy: ${score}%`;
        
        // Optional: Color the score
        document.getElementById("score").style.color = score > 80 ? "#4ade80" : "#f87171";

    } catch (error) {
        console.error(error);
        outputDiv.innerText = "Connection Error: Check if Backend is live.";
    }
}function copyText() {
    const text = document.getElementById("output").innerText;
    navigator.clipboard.writeText(text);
    alert("Corrected text copied!");
}
