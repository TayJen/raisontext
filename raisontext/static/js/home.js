const textInput = $('#main-textarea');
const classifyBtn = $('#submit-button');
const answerLbl = $("#answer-label");


classifyBtn.click(() => {
    console.log('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee');
    let text = textInput.val();
    console.log(text);

    $.ajax({
        url: 'http://127.0.0.1:8000/classify',
        data: JSON.stringify({'text': text}),
        method: 'post',
        contentType: "application/json",
        dataType: 'json',
        success: (result) => {
            console.log(result);
            statusUpload = result.status;
            if (statusUpload === 'null') {
                alert("Текст не может быть пустым");
            }
            else {
                answerLbl.empty();
                console.log(result.prediction)
                answerLbl.append(result.prediction);
            }
        },
        error: function(xhr, status, error) {
            console.log(xhr.responseText);
        }
    });
});
