const textInput = $('#main-textarea');
const classifyBtn = $('#submit-button');
const answerLbl = $("#answer-label");
const spinner = $(".lds-default");


var ws = new WebSocket(`ws://127.0.0.1:8000/classify`);
console.log("Connected")
ws.onmessage = function (event) {
    console.log(event.data);
    answerLbl.append(event.data);
    spinner.addClass("hidden");
};

function sendMessage(event) {
    answerLbl.empty();
    spinner.removeClass("hidden");

    let text = textInput.val();
    console.log(text);

    if (!text) {
        alert("Текст не может быть пустым");
    }

    ws.send(text);
}

classifyBtn.click(sendMessage);
