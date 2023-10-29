const textInput = $('#main-textarea');
const classifyBtn = $('#submit-button');
const answerLbl = $("#answer-label");


classifyBtn.click(() => {
    let text = textInput.value;
    console.log(text);

    $.ajax({
        url: 'http://127.0.0.1:8000/classify',
        data: JSON.stringify({'text': text}),
        method: 'post',
        processData: false,
        contentType: false,
        success: (result) => {
            console.log(result);
            statusUpload = result.status
            if (statusUpload === 'null') {
                alert("Текст не может быть пустым");
            }
            else {
                img.attr("src", `/static/images/${result.filename}`);
                filename = result.filename;
                imgPath = result.path;
            }
        },
        error: function(xhr, status, error) {
            console.log(xhr.responseText);
        }
    });
});
