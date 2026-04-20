async function checkGrammar() {
    const text = document.getElementById("inputText").value;
    const output = document.getElementById("output");
    const scoreBox = document.getElementById("score");

    if (!text.trim()) {
        alert("Please enter text");
        return;
    }

    output.innerText = "Checking...";
    scoreBox.innerText = "";

    try {
        const response = await fetch("https://ai-typo-corrector-ultra.onrender.com/correct", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        console.log(data); // debug

        output.innerText = data.corrected;
        scoreBox.innerText = `Score: ${data.score}/100`;

    } catch (error) {
        console.error(error);
        output.innerText = "❌ Backend not responding";
    }
}
