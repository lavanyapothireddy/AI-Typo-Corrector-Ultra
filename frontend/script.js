const API_URL = "https://ai-typo-corrector-ultra.onrender.com/correct";

async function checkGrammar() {
    const text = document.getElementById("inputText").value;
    const output = document.getElementById("output");
    const scoreBox = document.getElementById("score");

    if (!text.trim()) {
        output.innerText = "⚠️ Please enter text";
        return;
    }

    output.innerText = "⏳ Checking...";
    scoreBox.innerText = "";

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        const data = await res.json();

        if (data.error) {
            output.innerText = "❌ Error: " + data.error;
            return;
        }

        output.innerText = data.corrected;
        scoreBox.innerText = `📊 Score: ${data.score}/100`;

    } catch (err) {
        output.innerText = "❌ Backend not responding";
    }
}
