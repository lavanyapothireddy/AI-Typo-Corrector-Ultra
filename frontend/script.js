async function correctText() {
    const text = document.getElementById("input").value;

    if (!text) {
        alert("Please enter text");
        return;
    }

    document.getElementById("output").innerText = "Processing...";

    const res = await fetch("http://127.0.0.1:8000/correct", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
    });

    const data = await res.json();

    document.getElementById("output").innerHTML =
        "✨ Corrected Text:\n\n" + data.corrected +
        "\n\n-------------------\n" +
        "❌ Issues Found: " + data.issues_count;
}