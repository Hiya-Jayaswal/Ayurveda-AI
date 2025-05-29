function pro(msg) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://52.66.214.186/api/chat");
    xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    const body = JSON.stringify({
        'message': msg
    });
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            displayResponse(msg, xhr.responseText);
        } else {
            console.log(`Error: ${xhr.status}`);
        }
    };
    xhr.send(body);
}

function submitQuestion() {
    var question = document.getElementById("prompt").value;
    var formattedText = '<p class="bold">You:</p> ' + question;
    var messageElement = document.createElement("p");
    messageElement.innerHTML = formattedText;
    var messageContainer = document.getElementById("message-container");
    messageContainer.appendChild(messageElement);
    document.getElementById("prompt").value = "";

    // Send question to AI
    pro(question);

    // Show loading indicator after the user's message
    var loadingElement = document.getElementById("loading");
    messageContainer.appendChild(loadingElement);
}

function displayResponse(question, response) {
    var formattedResponse = '<p class="bold">Assistant:</p> ' + response.replace(/\n/g, "<br>");

    var messageElement = document.createElement("p");
    messageElement.innerHTML = formattedResponse;
    messageElement.classList.add("ai-message");
    var messageContainer = document.getElementById("message-container");
    messageContainer.appendChild(messageElement);
    messageContainer.scrollTop = messageContainer.scrollHeight;

    // Hide loading indicator
    var loadingElement = document.getElementById("loading");
    loadingElement.remove();
}

const promptInput = document.getElementById("prompt");

promptInput.addEventListener("keydown", function(event) {
    if (event.keyCode === 13) {
        submitQuestion();
    }
});
