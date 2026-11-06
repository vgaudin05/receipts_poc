const button = document.getElementById("testButton");
const result = document.getElementById("result");

button.addEventListener("click", async function() {

    result.textContent = "Connecting to database...";

    try {
        const response = await fetch("/api/poc");

        if (!response.ok) {
            throw new Error("Connection failed");
        }

        const data = await response.json();

        result.textContent = data.message;

    } catch (error) {
        result.textContent = "Unable to connect to database.";
    }

});
