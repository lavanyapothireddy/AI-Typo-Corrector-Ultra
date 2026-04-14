async function analyzeText() {
    const userInput = document.getElementById("input-text").value;
    const outputElement = document.getElementById("output-text");

    if (!userInput) {
        alert("Please enter some text!");
        return;
    }

    outputElement.innerText = "Analyzing...";

    try {
        // REPLACE with your actual Render URL
        const response = await fetch("https://ai-typo-corrector-ultra.onrender.com/correct", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            // 3. FIX: Sending "text" to match the Python BaseModel
            body: JSON.stringify({ text: userInput }),
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        console.log("Success:", data);

        // 4. FIX: Use data.corrected to match the Python return key
        outputElement.innerText = data.corrected;

    } catch (error) {
        console.error("Error:", error);
        outputElement.innerText = "Error: Could not connect to the server.";
    }
}
