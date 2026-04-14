async function analyzeText() {
    // 1. Get what the user typed
    const userInput = document.getElementById("input-text").value;
    const outputElement = document.getElementById("output-text");

    if (!userInput) {
        alert("Please enter some text!");
        return;
    }

    outputElement.innerText = "Analyzing...";

    try {
        // 2. Send the text to your Render Backend
        const response = await fetch("https://ai-typo-corrector-ultra.onrender.com/correct", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: userInput }),
        });

        // 3. Wait for the server to send the JSON answer back
        const data = await response.json();
        console.log("Success:", data);

        // --- THE LINE GOES HERE ---
        // This takes "data.corrected" from Python and puts it into your HTML div
        outputElement.innerText = data.corrected; 
        // ---------------------------

    } catch (error) {
        console.error("Error:", error);
        outputElement.innerText = "Error: Could not connect to the server.";
    }
}
