document.getElementById("user-input").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;
    
    appendMessage(userInput, "user");
    document.getElementById("user-input").value = "";

    // Show loading indicator
    const loadingIndicator = document.createElement("div");
    loadingIndicator.className = "loading-indicator";
    loadingIndicator.textContent = "Just a moment...";
    document.getElementById("chat-messages").appendChild(loadingIndicator);
    loadingIndicator.style.display = "block";

    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading indicator
        loadingIndicator.style.display = "none";
        appendMessage(data.response, "assistant");
    });
}

function appendMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add(sender);

    if (sender === 'assistant') {
        const formattedResponse = formatResponse(message);
        messageElement.innerHTML = formattedResponse;
    } else {
        messageElement.innerText = message;
    }

    const chatMessages = document.getElementById('chat-messages');
    chatMessages.appendChild(messageElement);
}

function formatResponse(response) {
    // Split the response into parts
    const parts = response.split(', ');

    // Check if the response has the expected number of parts for formatting
    if (parts.length >= 5) {
        const dateTime = parts[0] + ',';
        const teams = '<strong>' + parts[2].replace(' at Fanduel Sportsbook are as follows: - ', '') + '</strong>';
        const odds = parts[3].replace(' - ', '<br>- ') + '<br>' + parts[4].split(' ')[0];
        const note = parts[4].split(' ').slice(1).join(' ');

        // Format the response
        return `
            ${dateTime}<br>
            ${teams}<br>
            - ${odds}<br>
            ${note}
        `;
    } else {
        // If the response text is in a different format, return it as is
        return response;
    }
}





