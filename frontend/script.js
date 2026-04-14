async function analyze() {

    const text = document.getElementById("inputText").value;

    const res = await fetch("https://ai-typo-corrector-ultra.onrender.com/correct", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
    });

    const data = await res.json();

    document.getElementById("output").innerText = data.corrected;

    document.getElementById("wrong").innerText = data.wrong_words;
    document.getElementById("correct").innerText = data.correct_words;
    document.getElementById("total").innerText = data.total_words;
    document.getElementById("score").innerText = data.score;
}
