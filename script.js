async function askAI(type) {
    const topic = document.getElementById("topic").value.trim();
    const result = document.getElementById("result");
    const buttons = document.querySelectorAll(".buttons button");

    if (!topic) {
        result.textContent = "Please enter a study topic first!";
        return;
    }

    buttons.forEach((button) => {
        button.disabled = true;
    });
    result.textContent = "Working on your study material...";

    try {
        const response = await fetch("/api/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic, type }),
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "The request failed.");
        }

        result.textContent = data.answer;
    } catch (error) {
        result.textContent = error.message || "Could not connect to the server.";
    } finally {
        buttons.forEach((button) => {
            button.disabled = false;
        });
    }
}