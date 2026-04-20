async function checkGrammar() {
    const text = document.getElementById("inputText").value;

    if (!text.trim()) {
        alert("Please enter text");
        return;
    }

    try {
        const response = await fetch("https://ai-typo-corrector-ultra.onrender.com/correct", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        // 🔴 IMPORTANT CHECK
        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        console.log(data); // DEBUG

        document.getElementById("outputText").innerText = "✍️ " + data.corrected;
        document.getElementById("score").innerText = "📊 Score: " + data.score + "/100";

    } catch (error) {
        console.error(error);
        document.getElementById("outputText").innerText = "❌ Backend not responding";
        document.getElementById("score").innerText = "";
    }
}
